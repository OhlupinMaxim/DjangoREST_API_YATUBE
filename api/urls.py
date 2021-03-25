from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from .views import CommentViewSet
from .views import ReviewViewSet
from .views import EmailRegisterView, TokenView, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename="reviews")
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename="comments")

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/categories/',
        CategoryViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='category'
    ),
    path(
        'v1/categories/<slug:slug>/',
        CategoryViewSet.as_view({'delete': 'destroy', }),
        name='category_slug'
    ),
    path(
        'v1/genres/',
        GenreViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='genres'
    ),
    path(
        'v1/genres/<slug:slug>/',
        GenreViewSet.as_view({'delete': 'destroy', }),
        name='genres_slug'
    ),
    path(
        'v1/auth/email/',
        EmailRegisterView.as_view(),
        name='get_confirmation_code'
    ),
    path(
        'v1/auth/token/',
        TokenView.as_view(),
        name='get_token'
    )
]
