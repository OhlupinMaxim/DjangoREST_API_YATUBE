from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from comment.models import Comment
from review.models import Review
from title.filters import TitleFilter
from title.models import Category, Title, Genre
from user.models import User
from user.permissions import IsAdmin
from user.permissions import IsAdminOrReadOnly
from user.permissions import IsAuthorOrAdminOrModerator
from .serializers import CategorySerializer, GenreSerializer
from .serializers import CommentSerializer
from .serializers import ReviewSerializer
from .serializers import UserSerializer, YamdbRoleSerializer

from .serializers import (CodeEmailSerializer, UserEmailSerializer,
                          UserSerializer, YamdbRoleSerializer)
from .utils import send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = 'username'

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='me')
    def user_profile(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = YamdbRoleSerializer(user, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class EmailRegisterView(APIView):
    def post(self, request):
        serializer = UserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user, create = User.objects.get_or_create(email=email)
        if create:
            user.username = email
            user.save()
        conf_code = default_token_generator.make_token(user)
        send_confirmation_code(email, conf_code)
        return Response(
            f'Confirmation code will be sent to your {email}',
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    def post(self, request):
        serializer = CodeEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')
        user = get_object_or_404(User, email=email)
        if default_token_generator.check_token(user, code):
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorOrAdminOrModerator, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(
            author=self.request.user,
            title=title
        )

    def partial_update(self, request, *args, **kwargs):
        # title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        self.serializer_class.save(
            text=kwargs.get("text"),
            score=kwargs.get("score")
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorOrAdminOrModerator, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return Comment.objects.filter(
            title=title,
            review=review
        )

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(
            title=title,
            review=review,
            author=self.request.user
        )

    def partial_update(self, request, *args, **kwargs):
        # title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        # review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        self.serializer_class.save(
            text=kwargs.get("text")
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly, ]
    filterset_class = TitleFilter

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('review_title__score')).all().order_by('pk')


class EmailRegisterView(APIView):
    def post(self, request):
        serializer = UserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user, create = User.objects.get_or_create(email=email)
        if create:
            user.username = email
            user.save()
        conf_code = default_token_generator.make_token(user)
        send_confirmation_code(email, conf_code)
        return Response(
            f'Confirmation code will be sent to your {email}',
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    def post(self, request):
        serializer = CodeEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')
        user = get_object_or_404(User, email=email)
        if default_token_generator.check_token(user, code):
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
