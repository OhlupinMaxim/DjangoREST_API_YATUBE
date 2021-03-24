from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import User

from review.models import Review

from comment.models import Comment

from title.models import Category


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
        fields = 'name', 'slug'
        model = Category
