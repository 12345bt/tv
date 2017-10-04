from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=20)
    rating = models.CharField(max_length=4)
    genres = models.CharField(max_length=30)
    summary = models.CharField(max_length=305)
    movie_id = models.CharField(max_length=15)
    timeline = models.CharField(max_length=40)
    image = models.CharField(max_length=200)

    def __str__(self):
        return '{} {} / {}'.format(self.title, self.rating, self.genres)
