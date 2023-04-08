from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializer import BooksSerializer
from store.permissions import IsOwnerOrStaffOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    serializer_class = BooksSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['price',]
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


def oauth_view(request):
    if request.user:
        print(request.user.username)
    return render(request, 'oauth.html')
