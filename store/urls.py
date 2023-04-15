from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BookViewSet
from .views import oauth_view
from .views import UserBookRelationViewSet

router = DefaultRouter()

router.register(r'book', BookViewSet)
router.register(r'book-relation', UserBookRelationViewSet)

urlpatterns = router.urls

urlpatterns += [
        path('auth/', oauth_view, name='auth'),
        ]
