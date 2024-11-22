from django.core.management.base import BaseCommand
import pycountry
from pycountry_convert import country_alpha2_to_continent_code
from django.db import transaction
from posts.models import Country, Continent

CONTINENT_MAPPING = {
    'AF': 'Africa',
    'AS': 'Asia',
    'EU': 'Europe',
    'NA': 'North America',
    'SA': 'South America',
    'OC': 'Oceania',
    'AN': 'Antarctica',
}

class Command(BaseCommand):
    help = "Populate Continent and Country models with data from pycountry library"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Starting population of continents and countries...')

        # Populate Continents
        for code, name in CONTINENT_MAPPING.items():
            Continent.objects.get_or_create(continent_name=name)
            self.stdout.write(f"Added continent: {name}")

        # Populate Countries
        created_count = 0
        failed_count = 0

        # Pre-fetch all continents
        continents = {
            continent.continent_name: continent
            for continent in Continent.objects.all()
        }

        for country in pycountry.countries:
            try:
                # Get continent code using the correct function
                continent_code = country_alpha2_to_continent_code(country.alpha_2)  # Function call
                continent_name = CONTINENT_MAPPING[continent_code]
                continent = continents[continent_name]

                # Create country
                _, created = Country.objects.get_or_create(
                    country_name=country.name,
                    defaults={'continent': continent}
                )

                if created:
                    created_count += 1
                    self.stdout.write(f"Added country: {country.name} in {continent_name}")

            except KeyError:
                failed_count += 1
                self.stderr.write(
                    self.style.WARNING(f"Continent not found for country: {country.name}")
                )
            except Exception as e:
                failed_count += 1
                self.stderr.write(
                    self.style.ERROR(f"Error processing country {country.name}: {str(e)}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} new countries'
            )
        )

        if failed_count:
            self.stdout.write(
                self.style.WARNING(
                    f'Failed to create {failed_count} countries'
                )
            )
