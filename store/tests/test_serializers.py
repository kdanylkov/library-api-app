from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Book
from store.serializer import BooksSerializer


class BooksSerializerTestCase(TestCase):

    def test_serializer(self):
        user = User.objects.create(username='test username')

        book1 = Book.objects.create(
            name='Test', price=434.99, author_name='Test Author', owner=user)
        book2 = Book.objects.create(
            name='Test book 2', price=343.33, author_name='Test Author', owner=user)

        data = BooksSerializer([book1, book2], many=True).data

        expected_data = [
            {
                'id': book1.pk,
                'name': 'Test',
                'price': '434.99',
                'author_name': 'Test Author',
                'owner': user.pk,
                'readers': []
            },
            {
                'id': book2.pk,
                'name': 'Test book 2',
                'price': '343.33',
                'author_name': 'Test Author',
                'owner': user.pk,
                'readers': []
            }
        ]

        self.assertEqual(data, expected_data)
