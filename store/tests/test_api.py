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
from store.models import UserBookRelation
from store.serializer import BooksSerializer
from store.views import get_books_queryset


class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='Test User')
        self.book1 = Book.objects.create(
            name='Test', price=434.99, author_name='Author 1',
            owner=self.user1)
        self.book2 = Book.objects.create(
            name='Test book 2 Author 1', price=45, author_name='Author 3',
            owner=self.user1)
        self.book3 = Book.objects.create(
            name='Test book 3', price=45, author_name='Author 2',
            owner=self.user1)

    def tearDown(self):
        self.user1.delete()
        self.book1.delete()
        self.book2.delete()
        self.book3.delete()

    def test_get(self):

        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(HTTP_200_OK, response.status_code)

        books = get_books_queryset()
        serialized_data = BooksSerializer(books, many=True).data

        self.assertEqual(serialized_data, response.data)
        self.assertIn('rating', response.json()[0].keys())
        self.assertIn('likes', response.json()[0].keys())

    def test_get_filter(self):
        url = reverse('book-list')

        response = self.client.get(url, data={'price': 45})

        books = get_books_queryset().filter(
                id__in=(self.book3.pk, self.book2.pk))

        serialized_data = BooksSerializer(books, many=True).data
        self.assertEqual(response.data, serialized_data)

    def test_get_search(self):
        url = reverse('book-list')

        response = self.client.get(url, data={'search': 'Author 1'})

        books = get_books_queryset().filter(
                id__in=(self.book1.pk, self.book2.pk))

        serialized_data = BooksSerializer(books, many=True).data
        self.assertEqual(response.data, serialized_data)

    def test_get_single_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book2.pk})
        response = self.client.get(url)
        book = Book.objects.get(pk=self.book2.pk)

        self.assertEqual(response.data['name'], book.name)  # type:ignore
        self.assertEqual(response.data['author_name'],  # type:ignore
                         book.author_name)

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
        self.assertEqual(Book.objects.last().owner, self.user1)  # type:ignore

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

    def test_update_not_owner(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        user2 = User.objects.create(username='test_user2')

        self.client.force_login(user2)

        payload = {
            'name': self.book1.name,
            'price': 100.00,
            'author_name': self.book1.author_name
        }

        json_payload = dumps(payload)

        response = self.client.put(url, data=json_payload,
                                   content_type='application/json')

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.price, 100.00)

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
        self.assertEqual(Book.objects.count(), 2)

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

    def test_delete_if_not_owner(self):
        user2 = User.objects.create(username='Test User 2')
        self.client.force_login(user2)

        url = reverse('book-detail', kwargs={'pk': self.book2.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)

    def test_delete_if_not_owner_but_is_staff(self):
        user2 = User.objects.create(username='Test User 2', is_staff=True)
        self.client.force_login(user2)

        url = reverse('book-detail', kwargs={'pk': self.book2.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)


class BookRelationApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='Test User')
        cls.book1 = Book.objects.create(
            name='Test', price=434.99, author_name='Author 1', owner=cls.user1)
        cls.book2 = Book.objects.create(
            name='Test book 2', price=343.33, author_name='Author 1',
            owner=cls.user1)
        cls.book3 = Book.objects.create(
            name='Test book 3', price=45, author_name='Author 2',
            owner=cls.user1)

    def test_like_and_bookmark(self):
        url = reverse('userbookrelation-detail', args=(self.book1.pk,))
        payload = {
            'like': True
        }

        json_payload = dumps(payload)

        self.client.force_login(self.user1)
        response = self.client.patch(
            url, data=json_payload, content_type='application/json')

        self.assertEqual(HTTP_200_OK, response.status_code)

        relation = UserBookRelation.objects.get(
            user=self.user1, book=self.book1)

        self.assertTrue(relation.like)

        payload = {
            'in_bookmarks': True
        }

        json_payload = dumps(payload)

        response = self.client.patch(
            url, data=json_payload, content_type='application/json')

        self.assertEqual(HTTP_200_OK, response.status_code)
        relation.refresh_from_db()
        self.assertTrue(relation.in_bookmarks, True)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book1.pk,))
        payload = {
            'rate': 4
        }

        json_payload = dumps(payload)

        self.client.force_login(self.user1)
        response = self.client.patch(
            url, data=json_payload, content_type='application/json')

        self.assertEqual(HTTP_200_OK, response.status_code)

        relation = UserBookRelation.objects.get(
            user=self.user1, book=self.book1)

        self.assertEqual(relation.rate, 4)

    def test_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book1.pk,))
        payload = {
            'rate': 6
        }

        json_payload = dumps(payload)

        self.client.force_login(self.user1)
        response = self.client.patch(
            url, data=json_payload, content_type='application/json')

        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)

        relation = UserBookRelation.objects.get(
            user=self.user1, book=self.book1)

        self.assertEqual(relation.rate, None)
