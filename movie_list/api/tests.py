from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Movie
from datetime import datetime
from dateutil import parser


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_can_create_a_movie(self):
        body = {'name': 'Breaking the waves'}
        response = self.client.post(
            reverse('create'),
            body,
            format="json")
        response_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response_body)
        self.assertEqual(response_body['name'], 'Breaking the waves')
        self.assertEqual(response_body['director'], None)
        self.assertIn("date_created", response_body)
        self.assertIn("date_modified", response_body)

        stored_movie = Movie.objects.get(id=response_body['id'])
        self.assertEqual(response_body['id'], stored_movie.id)
        self.assertEqual(response_body['name'], stored_movie.name)
        self.assertEqual(response_body['director'], stored_movie.director)
        self.assertEqual(parser.parse(response_body['date_created']), stored_movie.date_created)
        self.assertEqual(parser.parse(response_body['date_modified']), stored_movie.date_modified)

        self.assertIn("date_created", response_body)
        self.assertIn("date_modified", response_body)




    def test_validates_input_when_creating_movie(self):
        before_count = Movie.objects.count()
        body = {}
        response = self.client.post(
            reverse('create'),
            body,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Movie.objects.count(), before_count)

    def test_allows_optional_fields(self):
        body = {'name': 'Breaking the waves', 'director': 'Lars von Trier'}
        response = self.client.post(
            reverse('create'),
            body,
            format="json")
        response_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        stored_movie = Movie.objects.get(id=response_body['id'])
        self.assertEqual(body['director'], stored_movie.director)

