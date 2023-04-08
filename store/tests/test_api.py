from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase
from rest_framework.utils.json import dumps

from store.models import Book
from store.serializer import BooksSerializer


class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='Test User')
        self.book1 = Book.objects.create(
            name='Test', price=434.99, author_name='Author 1')
        self.book2 = Book.objects.create(
            name='Test book 2', price=343.33, author_name='Author 1')
        self.book3 = Book.objects.create(
            name='Test book 3', price=45, author_name='Author 2')

    def tearDown(self):
        self.user1.delete()
        self.book1.delete()
        self.book2.delete()
        self.book3.delete()

    def test_get(self):

        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(HTTP_200_OK, response.status_code)

        serialized_data = BooksSerializer(
            [self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(serialized_data, response.data)  # type:ignore

    def test_create(self):
        url = reverse('book-list')

        payload = {
            'name': 'Test Book 4',
            'price': '544.99',
            'author_name': 'Test Author 2'
        }
        json_payload = dumps(payload)
        self.client.force_login(self.user1)

        response = self.client.post(
            url, data=json_payload, content_type='application/json')

        self.assertEqual(HTTP_201_CREATED, response.status_code)

    def test_create_unauthorized_user(self):
        url = reverse('book-list')

        payload = {
            'name': 'Test Book 4',
            'price': '544.99',
            'author_name': 'Test Author 2'
        }
        json_payload = dumps(payload)

        response = self.client.post(
            url, data=json_payload, content_type='application/json')

        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."})  # type:ignore

    def test_update(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.client.force_login(self.user1)

        payload = {
            'name': self.book1.name,
            'price': 100.00,
            'author_name': self.book1.author_name
        }

        json_payload = dumps(payload)

        response = self.client.put(url, data=json_payload,
                                   content_type='application/json')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.price, 100.00)

    def test_update_insufficient_data(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.client.force_login(self.user1)

        payload = {
            'name': 'New name',
            'price': 1000.00
        }

        json_payload = dumps(payload)

        response = self.client.put(url, data=json_payload,
                                   content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['author_name'], [  # type:ignore
                         'This field is required.'])

    def test_delete(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.client.force_login(self.user1)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book1.pk)

    def test_partial_update(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.client.force_login(self.user1)

        payload = {
            'price': 150.00,
        }

        json_payload = dumps(payload)

        response = self.client.patch(url, data=json_payload,
                                     content_type='application/json')

        self.assertEqual(response.status_code, HTTP_200_OK)
        name, author_name = self.book1.name, self.book1.author_name

        self.book1.refresh_from_db()
        name_after_update, author_name_after_update = self.book1.name, self.book1.author_name

        self.assertEqual(self.book1.price, 150.00)
        self.assertEqual(name, name_after_update)
        self.assertEqual(author_name, author_name_after_update)
