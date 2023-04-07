from store.models import Book
from store.serializer import BooksSerializer

from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK

from django.urls import reverse


class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.book1 = Book.objects.create(name='Test', price=434.99, author_name='Author 1')
        self.book2 = Book.objects.create(name='Test book 2', price=343.33, author_name='Author 1')
        self.book3 = Book.objects.create(name='Test book 3', price=45, author_name='Author 2')
        
    def test_get(self):

        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(HTTP_200_OK, response.status_code)

        serialized_data = BooksSerializer([self.book1, self.book2], many=True).data
        self.assertEqual(serialized_data, response.data)

