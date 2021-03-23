from django.db import models

from review.models import Review

from user.models import User


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name="comment_review")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="comment_author")
    pub_date = models.DateTimeField("Дата Публикации",
                                    auto_now_add=True,
                                    db_index=True)
    text = models.TextField
