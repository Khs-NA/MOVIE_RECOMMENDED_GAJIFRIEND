from django.db import models
from django.conf import settings

# Create your models here.


# 전체 영화
class Movie(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.DateTimeField()
    overview = models.TextField()
    poster_path = models.TextField()
    vote_average = models.FloatField()
    genres = models.CharField(max_length=50)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')

    def __str__(self):
        return self.title

# 현재 상영작
class Movie_New(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.DateTimeField()
    overview = models.TextField()
    poster_path = models.TextField()
    vote_average = models.FloatField()
    genres = models.CharField(max_length=50)

