from django.db import models

from review.models import Review
from title.models import Title
from user.models import User


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comment_review',
                               blank=True,
                               null=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='comment_title',
                              blank=True,
                              null=True)

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comment_author',
                               null=True,
                               blank=True)
    pub_date = models.DateTimeField('Дата Публикации',
                                    auto_now_add=True,
                                    db_index=True)
    text = models.TextField(null=False, blank=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:15]