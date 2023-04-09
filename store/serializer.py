from rest_framework.serializers import ModelSerializer

from store.models import Book
from store.models import UserBookRelation


class BooksSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class UserBookRelationsSerializer(ModelSerializer):

    class Meta:
        model = UserBookRelation
        fields = 'book', 'like', 'in_bookmarks', 'rate'
