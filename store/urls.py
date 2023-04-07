from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BookViewSet
from .views import oauth_view

router = DefaultRouter()
router.register(r'book', BookViewSet)
urlpatterns = router.urls

urlpatterns.append(path('auth/', oauth_view, name='auth'))
