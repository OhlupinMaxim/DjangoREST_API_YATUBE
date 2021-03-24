from django.db import models


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField('Genre', related_name='titles', blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name
