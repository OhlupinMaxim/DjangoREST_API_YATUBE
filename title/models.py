import textwrap
from datetime import date

from django.core.validators import MaxValueValidator
from django.db import models


class Title(models.Model):
    """
    Модель Title(Произведение).
    Поля:
    name - 'Название произведения', обязательное.
    year - 'Год', обязательное, значение по умолчанию 0, валидируемое не может
    быть больше текущего года.
    description - 'Описание произведения', необязательное.
    category - 'Категория', внешний ключ на модель Category, необязательное.
    genre - 'Жанр', внешний ключ на модель Genre, множественное,
    необязательное.
    Сортровка - primary key.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Год',
        validators=[MaxValueValidator(date.today().year)]
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='titles',
        blank=True,
        verbose_name='Жанры'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('pk',)

    def __str__(self):
        return textwrap.shorten(self.name, 15, placeholder='...')


class Category(models.Model):
    """
    Модель Category(Категория).
    Поля:
    name - 'Название категории', обязательное.
    slug - 'Путь категории', обязательное.
    Сорторовка - slug.
    """
    name = models.CharField(max_length=200, verbose_name='Название категории')
    slug = models.SlugField(
        max_length=20,
        unique=True,
        verbose_name='Путь категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Модель Genre(Жанр).
    Поля:
    name - 'Название жанра', обязательное.
    slug - 'Путь жанра', обязательное.
    Сорторовка - slug.
    """
    name = models.CharField(max_length=200, verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=20,
        unique=True,
        verbose_name='Путь жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('slug',)

    def __str__(self):
        return self.name
