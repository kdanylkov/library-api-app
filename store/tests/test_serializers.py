from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Book, UserBookRelation
from store.serializer import BooksSerializer
from store.views import get_books_queryset


class BooksSerializerTestCase(TestCase):

    def test_serializer(self):
        user1 = User.objects.create_user(
                username='testuser1',
                first_name='first_name1',
                last_name='last_name1'
                )
        user2 = User.objects.create_user(
                username='testuser2',
                first_name='first_name2',
                last_name='last_name2'
                )
        user3 = User.objects.create_user(
                username='testuser3',
                first_name='first_name3',
                last_name='last_name3'
                )

        book1 = Book.objects.create(
            name='Test', price=434.99, author_name='Test Author', owner=user1)
        book2 = Book.objects.create(
            name='Test book 2', price=343.33, author_name='Test Author',
            owner=user2)

        UserBookRelation.objects.create(book=book1, user=user1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(book=book1, user=user2, like=True,
                                        rate=5)
        UserBookRelation.objects.create(book=book1, user=user3, like=True,
                                        rate=4)

        UserBookRelation.objects.create(book=book2, user=user1, like=True,
                                        rate=4)
        UserBookRelation.objects.create(book=book2, user=user2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(book=book2, user=user3, like=False)

        books = get_books_queryset()
        data = BooksSerializer(books, many=True).data

        expected_data = [
            {
                'id': book1.pk,
                'name': 'Test',
                'price': '434.99',
                'author_name': 'Test Author',
                'likes': 3,
                'rating': '4.67',
                'owner_name': 'testuser1',
                'readers': [
                    {
                        'first_name': 'first_name1',
                        'last_name': 'last_name1'
                        },
                    {
                        'first_name': 'first_name2',
                        'last_name': 'last_name2'
                        },
                    {
                        'first_name': 'first_name3',
                        'last_name': 'last_name3'
                        }
                    ]
            },
            {
                'id': book2.pk,
                'name': 'Test book 2',
                'price': '343.33',
                'author_name': 'Test Author',
                'likes': 2,
                'rating': '3.50',
                'owner_name': 'testuser2',
                'readers': [
                    {
                        'first_name': 'first_name1',
                        'last_name': 'last_name1'
                        },
                    {
                        'first_name': 'first_name2',
                        'last_name': 'last_name2'
                        },
                    {
                        'first_name': 'first_name3',
                        'last_name': 'last_name3'
                        }

                    ]
            }
        ]

        self.assertEqual(data, expected_data)
