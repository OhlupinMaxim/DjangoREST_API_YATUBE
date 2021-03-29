from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.FilterSet):
    """
    Фильтр для поиска произведений:
    Сортировка по полю slug(Путь жанра) модели Genre(Жанр), точное соотвествие.
    Сортировка по полю slug(Путь категории) модели Category(Категория),
    точное соотвествие.
    Сортировка по полю name(Название произведения) модели Title(Произведение),
    не точное соотвестие - содержит.
    Сортировка по полю year(Год) модели Title(Произведение),точное соотвествие.
    """
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year']
