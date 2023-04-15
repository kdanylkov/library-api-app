from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg

from store.models import Book, UserBookRelation
from store.serializer import BooksSerializer


class BooksSerializerTestCase(TestCase):

    def test_serializer(self):
        user1 = User.objects.create_user(username='testuser1')
        user2 = User.objects.create_user(username='testuser2')
        user3 = User.objects.create_user(username='testuser3')

        book1 = Book.objects.create(
            name='Test', price=434.99, author_name='Test Author')
        book2 = Book.objects.create(
            name='Test book 2', price=343.33, author_name='Test Author')

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

        books = Book.objects.all().annotate(
                annotated_likes=Count(
                    Case(
                        When(userbookrelation__like=True, then=1)
                        )
                    ),
                rating=Avg('userbookrelation__rate')
                ).order_by('id')

        data = BooksSerializer(books, many=True).data

        expected_data = [
            {
                'id': book1.pk,
                'name': 'Test',
                'price': '434.99',
                'author_name': 'Test Author',
                'likes_count': 3,
                'annotated_likes': 3,
                'rating': '4.67'
            },
            {
                'id': book2.pk,
                'name': 'Test book 2',
                'price': '343.33',
                'author_name': 'Test Author',
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': '3.50'
            }
        ]

        self.assertEqual(data, expected_data)
