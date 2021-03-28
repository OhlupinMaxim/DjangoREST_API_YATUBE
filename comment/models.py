from django.db import models

from review.models import Review
from title.models import Title
from user.models import User


class Comment(models.Model):
    """
    Модель Comment(Комменарий). Комментарий на отзыв о произведении.
    Поле review(Отзыв) внешний ключ на модель Review(Отзыв).
    Поле title(Произведение) внешний ключ на модель Title(Произведение).
    Поле author(Автор) внешний ключ на модель User(Пользователь).
    Поле pub_date(Дата публикации), cоздается автоматически.
    Поле text(Текст Комментария).
    """
    review = models.ForeignKey(Review,
                               verbose_name='Отзыв',
                               on_delete=models.CASCADE,
                               related_name='comment_review',
                               blank=True,
                               null=True)
    title = models.ForeignKey(Title,
                              verbose_name='Произведение',
                              on_delete=models.CASCADE,
                              related_name='comment_title',
                              blank=True,
                              null=True)

    author = models.ForeignKey(User,
                               verbose_name='Автор комментария',
                               on_delete=models.CASCADE,
                               related_name='comment_author',
                               null=True,
                               blank=True)
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)
    text = models.TextField(verbose_name='Текст Комментария',
                            null=False,
                            blank=True)

    class Meta:
        verbose_name = 'Коммеентарий'
        verbose_name_plural = 'Коммеентарии'
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:15]
