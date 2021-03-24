from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet
from .views import CommentViewSet
from .views import ReviewViewSet
from .views import UserViewSet

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, 'users')

"""
    урлы для других моделей туточки
"""

router_v1.register(
    "r'titles/(?P<title_id>\d+)/reviews'",
    ReviewViewSet,
    "reviews")
router_v1.register(
    "r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments'",
    CommentViewSet,
    "comments")

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/categories/',
        CategoryViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='Category'
    ),
    path(
        'v1/categories/<slug:slug>/',
        CategoryViewSet.as_view({'delete': 'destroy', }),
        name='Category'
    ),
    path(
        'v1/genres/',
        CategoryViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='Category'
    ),
    path(
        'v1/genres/<slug:slug>/',
        CategoryViewSet.as_view({'delete': 'destroy', }),
        name='Category'
    ),
]
