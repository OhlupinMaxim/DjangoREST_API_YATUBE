from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.permissions import IsAdmin
from user.permissions import IsAuthorOrAdminOrModerator

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
        title_id = self.kwargs.get("title_id")
        pass

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        pass

    def partial_update(self, request, *args, **kwargs):
        title_id = self.kwargs.get("title_id")
        pass


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorOrAdminOrModerator, ]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        pass

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        pass

    def partial_update(self, request, *args, **kwargs):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        pass
