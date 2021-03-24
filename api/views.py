from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.permissions import IsAdmin
from user.permissions import IsAuthorOrAdminOrModerator

from title.models import Title
from title.models import Category
from title.models import Genre

from review.models import Review

from comment.models import Comment

from .serializers import UserSerializer, YamdbRoleSerializer
from .serializers import CommentSerializer
from .serializers import ReviewSerializer


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
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = YamdbRoleSerializer(user, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


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
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        pass


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
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        pass
