from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import Bucket
from dateutil import parser


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_can_create_a_bucket(self):
        body = {'name': 'My bucket'}
        response = self.client.post(
            reverse('bucket.create'),
            body,
            format="json")
        response_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response_body)
        self.assertEqual(response_body['name'], 'My bucket')
        self.assertIn("date_created", response_body)
        self.assertIn("date_modified", response_body)

        stored_bucket = Bucket.objects.get(id=response_body['id'])
        self.assertEqual(response_body['id'], stored_bucket.id)
        self.assertEqual(response_body['name'], stored_bucket.name)
        self.assertEqual(parser.parse(response_body['date_created']), stored_bucket.date_created)
        self.assertEqual(parser.parse(response_body['date_modified']), stored_bucket.date_modified)

        self.assertIn("date_created", response_body)
        self.assertIn("date_modified", response_body)

    def test_validates_input_when_creating_bucket(self):
        before_count = Bucket.objects.count()
        body = {}
        response = self.client.post(
            reverse('bucket.create'),
            body,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Bucket.objects.count(), before_count)

    def test_can_retrieve_a_bucket(self):
        bucket = Bucket.objects.create(name='My bucket')
        response = self.client.get(
            reverse('bucket.details', kwargs={'pk': bucket.id}),
            format="json")
        response_body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['id'], bucket.id)
        self.assertEqual(response_body['name'], bucket.name)
        self.assertEqual(parser.parse(response_body['date_created']), bucket.date_created)
        self.assertEqual(parser.parse(response_body['date_modified']), bucket.date_modified)

    def test_can_update_a_bucket(self):
        new_bucket = Bucket.objects.create(name='To Watch')
        bucket_changes = {'name': 'To Watch'}
        response = self.client.put(
            reverse('bucket.details', kwargs={'pk': new_bucket.id}),
            data=bucket_changes,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bucket = Bucket.objects.get(id=new_bucket.id)
        self.assertEquals(bucket.name, bucket_changes['name'])

    def test_can_delete_a_bucket(self):
        bucket_to_be_deleted = Bucket.objects.create(name='To Watch')
        response = self.client.delete(
            reverse('bucket.details', kwargs={'pk': bucket_to_be_deleted.id}),
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Bucket.objects.filter(id=bucket_to_be_deleted.id).count(), 0)

    def test_handles_movie_not_found(self):
        response = self.client.get(
            reverse('bucket.details', kwargs={'pk': 999}),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
