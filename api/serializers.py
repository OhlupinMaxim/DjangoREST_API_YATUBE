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


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class CodeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field="id",
                                         read_only=True)

    class Meta:
        fields = ['id', 'text', 'author', 'title', 'score', 'pub_date']
        model = Review

    def validate(self, attrs):
        user = self.context["request"].user
        title_id = str(self.context["request"].META["PATH_INFO"]).split("/")[4]
        title = Title.objects.filter(
            id=title_id).first()
        reviews = Review.objects.filter(
            author=user,
            title=title
        )
        if reviews.count() > 0:
            if self.context["request"].META['REQUEST_METHOD'] == "POST":
                raise serializers.ValidationError("Уже существует")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field="id",
                                         read_only=True)

    review = serializers.SlugRelatedField(slug_field="id",
                                          read_only=True)

    class Meta:
        fields = "__all__"
        model = Comment

    def validate(self, attrs):
        if self.context["request"].META['REQUEST_METHOD'] == "POST":
            if len(attrs) == 0:
                raise serializers.ValidationError
        return attrs


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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
