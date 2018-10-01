from rest_framework import serializers
from .models import Movie, Bucket


class MovieSerializer(serializers.ModelSerializer):
    """ JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Movie
        fields = ('id', 'name', 'director', 'release_year', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')


class BucketSerializer(serializers.ModelSerializer):
    """ JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Bucket
        fields = ('id', 'name', 'movies', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')
