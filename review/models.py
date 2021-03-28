from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from title.models import Title
from user.models import User


class Review(models.Model):
    """
    Модель Review(Отзыв).
    Поле author(Автор) внешний ключ на модель User(Пользователь).
    Поле title(Произведение) внешний ключ на модель Title(Произведение).
    Поле pub_date(Дата публикации), cоздается автоматически.
    Поле score(Оценка), оценка на произведение.
    Поле text(Текст Отзыва).
    """
    author = models.ForeignKey(
        User,
        verbose_name='Автор Отзыва',
        on_delete=models.CASCADE,
        related_name='review_author',
        blank=True,
        null=True)
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='review_title',
        blank=True,
        null=True)
    pub_date = models.DateTimeField(
        verbose_name='Дата Публикации',
        auto_now_add=True,
        db_index=True)
    score = models.IntegerField(
        verbose_name='Оценка',
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    text = models.TextField(verbose_name='Текст отзыва')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:15]
