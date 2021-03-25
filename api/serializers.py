from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from comment.models import Comment
from review.models import Review
from title.models import Category, Genre, Title
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        default=email
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )


class YamdbRoleSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = "__all__"
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = "__all__"
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategoryRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return CategorySerializer(obj).data


class GenreRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return GenreSerializer(obj).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreRelatedField(slug_field='slug', queryset=Genre.objects.all(),
                              many=True)
    category = CategoryRelatedField(slug_field='slug',
                                    queryset=Category.objects.all())
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        return obj.rating