import django_filters
from posts.models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    body = django_filters.CharFilter(lookup_expr='icontains')
    owner = django_filters.CharFilter(field_name='owner__id', lookup_expr='icontains')
    country_name = django_filters.CharFilter(field_name='country__country_name', lookup_expr='icontains')
    created_at = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Post
        fields = ['title', 'body', 'owner', 'country_name', 'created_at']
