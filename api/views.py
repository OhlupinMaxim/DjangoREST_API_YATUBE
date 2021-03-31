from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from comment.models import Comment
from review.models import Review
from title.filters import TitleFilter
from title.models import Category, Genre, Title
from user.models import User
from user.permissions import (IsAdmin, IsAdminOrReadOnly,
                              IsAuthorOrAdminOrModerator)
from .serializers import (CategorySerializer, CodeEmailSerializer,
                          CommentSerializer, GenreSerializer, ReviewSerializer,
                          TitleSerializer, UserEmailSerializer, UserSerializer,
                          YamdbRoleSerializer)
from .utils import send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet класс для модели User.
    Разрешения: IsAdmin, IsAuthenticated
    Реализует HTTP методы: GET, POST, PATCH, DELETE

    Администратор может:

    * Получить список всех пользователей. (GET)
        (Вернет 200 и список пользователей, или ошибку 401)
    * Получить пользователя по его `username`. (GET)
        (Вернет 200 и данные пользователя, или ошибки 401/403/404)
    * Создать/изменить/удалить пользователя. (POST/PATCH/DELETE)
        (Вернет 200 при успешном запросе, или ошибки 400/401/403/404)

    Авторизованный пользователь может:

    * Получить данные своей учетной записи. (GET)
        (Вернет 200 и объект учетной записи, или ошибку 400)
    * Изменить данные своей учетной записи. (PATCH)
        (Вернет 200 при успешном запросе, или ошибку 400)
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
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
    """
    Класс APIView для получения confirmation_code по
        email пользователя

    Возвращает:
    * статус 200, отправляет код подтверждение на email пользователя
    * статус 400, если email не указан
    """

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
    """
    Класс APIView для получения access токена для
        доступа к ресурсам API

    Возвращает:
    * статус 200 и сгенерированный token
    * статус 400, если не указан email или
        указан неверный confirmation_code
    """

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
    """
    ViewSet класс для модели Review.
    Разрешения: IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator.
    Реализует HTTP методы: GET, POST, PATCH, DELETE.

    Получить все отзывы может любой пользователь. (GET)
        (Вернет список с пагинацей (статус 200) или статус 404 если не найдено)

    Получить отзыв по id может любой пользователь. (GET)
        (Вернет отзыв (статус 200) или статус 404 если не найдено)

    Создать отзыв может только Аунтифицированный пользователь. (POST)
        (Успешно создан (статус 200) вернет созданный отзыв.
        Нет токена (пользовтель не аунтифицирован (статус 401).
        Объект оценки не найден (статус 404).
        Неверные данные (статус 400))

    Частично обновить отзыв по id могут :
                                    Автор, Модератор, Администратор. (PATCH)
        (Успешно изменен (статус 200) вернет созданный отзыв.
        Нет токена (пользовтель не аунтифицирован (статус 401).
        Нет доступа (у пользователя нет прав (статус 403)).
        Объект оценки не найден (статус 404).
        Неверные данные (статус 400).)
    Удалить отзыв по id могут : Автор, Модератор, Администратор. (DELETE)
        (Успешно удален (статус 200).
        Нет токена (пользовтель не аунтифицирован (статус 401).
        Нет доступа (у пользователя нет прав (статус 403)).
        Объект оценки не найден (статус 404).)
    """
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerator,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet класс для модели Comment.
    Разрешения: IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator.
    Реализует HTTP методы: GET, POST, PATCH, DELETE.

    Получить все комментарии по id отзыва может любой пользователь (GET).
        (Вернет список с пагинацей (статус 200) или статус 404 если не найдено)

    Получить по id отзыва комментарий по id может любой пользователь (GET).
        (Вернет отзыв (статус 200) или статус 404 если не найдено)

    Создать комментарий может только Аунтифицированный пользователь. (POST)
        (Успешно создан (статус 200) вернет созданный отзыв.
        Нет токена (пользовтель не аунтифицирован (статус 401).
        Объект оценки не найден (статус 404).
        Неверные данные (статус 400))

    Частично обновить комментарий по id могут :
                                    Автор, Модератор, Администратор. (PATCH)
        (Успешно изменен (статус 200) вернет созданный комментарий.
        Нет токена (пользовтель не аунтифицирован (статус 401).
        Нет доступа (у пользователя нет прав (статус 403)).
        Объект оценки не найден (статус 404).
        Неверные данные (статус 400).)
    Удалить комментарий по id могут : Автор, Модератор, Администратор. (DELETE)
        (Успешно удален (статус 200).
        Нет токена (пользовтель не аунтифицирован (статус 401).
        Нет доступа (у пользователя нет прав (статус 403)).
        Объект оценки не найден (статус 404).)
    """
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerator,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return Comment.objects.filter(
            title=title,
            review=review
        )

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            title=title,
            review=review
        )


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet для Category(Категория).Отдельный объект возвращает на
    основе slug(Путь категории).
    Права доступа: администратор - чтение и запись, остальные - только чтение.
    Поиск: по полю name.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet для Genre(Жанр).Отдельный объект возвращает на
    основе slug(Путь жанра).
    Права доступа: администратор - чтение и запись, остальные - только чтение.
    Поиск: по полю name.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet для Title(Произведение).
    Права доступа: администратор - чтение и запись, остальные - только чтение.
    Поиск: по genre__slug, category__slug, year, name.
    Возвращает дополнительное значение rating - серднее значение всех объектов,
    модели Review(Отзыв), отнесенных к объекту модели Title(Произведение).
    """
    queryset = Title.objects.annotate(
        rating=Avg('review_title__score')).all().order_by('pk')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
