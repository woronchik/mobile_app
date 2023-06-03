from rest_framework import serializers

from posts.models import Post, Reply, Favorite
from users.models import UserProfile


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "photo",
            "title",
            "execution_date",
            "budget",
            "city",
        )


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "photo",
            "title",
            "budget",
            "other_details",
        )

class ReplyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "name",
            "city",
            "height",
            "bust",
            "waist",
            "hips",
            "clothes_size",
            "shoes_size"
        )


class ReplyListSerializer(serializers.ModelSerializer):
    from_person = ReplyProfileSerializer()

    class Meta:
        model = Reply
        fields = "__all__"


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = (
            "id",
            "from_person",
            "on_post",
        )


class ReplyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = (
            "id",
            "acceptance_status",
        )


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            "favorite_posts",
            "favorite_models",
        )
