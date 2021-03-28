from django.contrib.auth.models import AbstractUser
from django.db import models


class YamdbRoles(models.TextChoices):
    USER = ('user', 'user',)
    ADMIN = ('admin', 'admin',)
    MODERATOR = ('moderator', 'moderator',)


class User(AbstractUser):
    bio = models.TextField(max_length=200, blank=True)
    role = models.CharField(
        max_length=40,
        choices=YamdbRoles.choices,
        default=YamdbRoles.USER
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
        ordering = ('id',)
