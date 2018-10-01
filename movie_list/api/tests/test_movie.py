from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import Movie
from dateutil import parser


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_can_create_a_movie(self):
        body = {'name': 'Breaking the waves'}
        response = self.client.post(
            reverse('movie.create'),
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
            reverse('movie.create'),
            body,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Movie.objects.count(), before_count)

    def test_allows_optional_fields(self):
        body = {'name': 'Breaking the waves', 'director': 'Lars von Trier'}
        response = self.client.post(
            reverse('movie.create'),
            body,
            format="json")
        response_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        stored_movie = Movie.objects.get(id=response_body['id'])
        self.assertEqual(body['director'], stored_movie.director)

    def test_can_retrieve_a_movie(self):
        movie = Movie.objects.create(name='Manderlay', director='Lars von Trier', release_year=2005)
        response = self.client.get(
            reverse('movie.details', kwargs={'pk': movie.id}),
            format="json")
        response_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['id'], movie.id)
        self.assertEqual(response_body['name'], movie.name)
        self.assertEqual(response_body['director'], movie.director)
        self.assertEqual(parser.parse(response_body['date_created']), movie.date_created)
        self.assertEqual(parser.parse(response_body['date_modified']), movie.date_modified)


    def test_can_update_a_movie(self):
        new_movie = Movie.objects.create(name='Manderley', director='Lars von Trier', release_year=2005)
        movie_changes = {'name': 'Manderlay'}
        response = self.client.put(
            reverse('movie.details', kwargs={'pk': new_movie.id}),
            data=movie_changes,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movie = Movie.objects.get(id=new_movie.id)
        self.assertEquals(movie.name, movie_changes['name'])

    def test_can_delete_a_movie(self):
        movie_to_be_deleted = Movie.objects.create(name='Manderley', director='Lars von Trier', release_year=2005)
        response = self.client.delete(
            reverse('movie.details', kwargs={'pk': movie_to_be_deleted.id}),
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Movie.objects.filter(id=movie_to_be_deleted.id).count(), 0)

    def test_handles_movie_not_found(self):
        response = self.client.get(
            reverse('movie.details', kwargs={'pk': 999}),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
