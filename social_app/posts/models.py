from django.db import models
from users.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(CustomUser, related_name="liked_posts", blank=True)
    dislikes = models.ManyToManyField(CustomUser, related_name="disliked_posts", blank=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)  
    impressions = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.title

    def get_continent(self):
        return self.country.continent if self.country else None

    def like_count(self):
        return self.likes.count()

    def dislike_count(self):
        return self.dislikes.count()

    def comment_count(self):
        return self.comments.count()

    def view_count(self):
        return self.views

    def impression_count(self):
        return self.impressions

    def increment_views(self):
        self.views += 1
        self.save()

    def increment_impressions(self):
        self.impressions += 1
        self.save()


class Continent(models.Model):
    continent_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.continent_name


class Country(models.Model):
    country_name = models.CharField(max_length=255, unique=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, related_name='countries')

    def __str__(self):
        return self.country_name

class Comment(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    def __str__(self):
        return self.body
