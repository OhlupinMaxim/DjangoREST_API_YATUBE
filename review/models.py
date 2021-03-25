from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.db import models

from user.models import User

from title.models import Title


class Review(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="review_author",
                               blank=True,
                               null=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name="review_title",
                              blank=True,
                              null=True)
    pub_date = models.DateTimeField("Дата Публикации",
                                    auto_now_add=True,
                                    db_index=True)
    score = models.IntegerField(default=1,
                                validators=[
                                    MaxValueValidator(10),
                                    MinValueValidator(1)
                                ])
    text = models.TextField()

    def __str__(self):
        return self.text[:15]
