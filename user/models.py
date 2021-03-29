from django.contrib.auth.models import AbstractUser
from django.db import models


class YamdbRoles(models.TextChoices):
    """
    Список ролей пользователей Yamdb API,
    """
    USER = ('user', 'user',)
    ADMIN = ('admin', 'admin',)
    MODERATOR = ('moderator', 'moderator',)


class User(AbstractUser):
    """
    Модель User(Пользователи),
    на основе встроенной Django-модели AbstractUser,
    дополненная полями bio и role
    """
    bio = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='Информация о пользователе'
    )
    role = models.CharField(
        max_length=40,
        choices=YamdbRoles.choices,
        default=YamdbRoles.USER,
        verbose_name='Роль пользователя'
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (self.role == YamdbRoles.ADMIN
                or self.is_staff or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == YamdbRoles.MODERATOR

    class Meta(AbstractUser.Meta):
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('id', )
