from rest_framework.serializers import ModelSerializer
from .models import UserBookRelation

from store.models import Book
from rest_framework import serializers


class BooksSerializer(ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2,
                                      read_only=True)
    owner_name = serializers.CharField(source='owner.username',
                                       read_only=True, default='')

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name',
                  'likes', 'rating', 'owner_name')


class UserBookRelationsSerializer(ModelSerializer):

    class Meta:
        model = UserBookRelation
        fields = 'book', 'like', 'in_bookmarks', 'rate'
