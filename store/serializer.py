from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserBookRelation

from store.models import Book
from rest_framework import serializers


class BookReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BooksSerializer(ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2,
                                      read_only=True)
    owner_name = serializers.CharField(source='owner.username',
                                       read_only=True, default='')
    readers = BookReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name',
                  'likes', 'rating', 'owner_name', 'readers')


class UserBookRelationsSerializer(ModelSerializer):

    class Meta:
        model = UserBookRelation
        fields = 'book', 'like', 'in_bookmarks', 'rate'
