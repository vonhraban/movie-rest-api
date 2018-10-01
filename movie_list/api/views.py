from rest_framework import generics
from .serializers import MovieSerializer, BucketSerializer
from .models import Movie, Bucket


class MovieCreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class MovieDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class BucketCreateView(generics.ListCreateAPIView):
    serializer_class = BucketSerializer
    queryset = Bucket.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class BucketDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer
