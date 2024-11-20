from django.db import models
from users.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(CustomUser, related_name="liked_posts", blank=True)  # Tracks users who liked this post
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_continent(self):
        return self.country.continent if self.country else None


class Continent(models.Model):
    continent_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.continent_name


class Country(models.Model):
    country_name = models.CharField(max_length=255, unique=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, related_name='countries')

    def __str__(self):
        return self.country_name
