from django.db.models import Count, Case, When
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .models import UserBookRelation
from .serializer import BooksSerializer
from .serializer import UserBookRelationsSerializer
from store.permissions import IsOwnerOrStaffOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(
                annotated_likes=Count(
                    Case(
                        When(userbookrelation__like=True, then=1)
                        )
                    )
                ).order_by('id')

    permission_classes = [IsOwnerOrStaffOrReadOnly]
    serializer_class = BooksSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['price',]
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationsSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(
            user=self.request.user, book_id=self.kwargs['book'])
        return obj


def oauth_view(request):
    if request.user:
        print(request.user.username)
    return render(request, 'oauth.html')
