from rest_framework import generics
from .serializers import MovieSerializer
from .models import Movie


class CreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()


    def perform_create(self, serializer):
        serializer.save()


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
