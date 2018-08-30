from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
