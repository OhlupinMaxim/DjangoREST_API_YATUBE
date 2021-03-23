from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet
from .views import ReviewViewSet
from .views import CommentViewSet

router = DefaultRouter()

router.register('users', UserViewSet, 'users')

"""
    урлы для других моделей туточки
"""

router.register(
    "r'titles/(?P<title_id>\d+)/reviews'",
    ReviewViewSet,
    "reviews")
router.register(
    "r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments'",
    CommentViewSet,
    "comments")

urlpatterns = [
    path('', include(router.urls)),
]
