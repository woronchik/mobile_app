from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser

from posts.models import Post, Reply, Favorite
from posts.serializers import (PostSerializer, PostListSerializer, PostUpdateSerializer,
                               ReplyListSerializer, ReplyUpdateSerializer, ReplyCreateSerializer,
                               FavoriteSerializer, FavoriteUpdateSerializer)


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    queryset = Post.objects.all()
    serializer_classes = {
        "list": PostListSerializer,
        "update": PostUpdateSerializer,
    }
    http_method_names = ('get', 'delete', 'post', 'put')
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, PostSerializer)


class ReplyViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    queryset = Reply.objects.prefetch_related().all()
    serializer_classes = {
        "create": ReplyCreateSerializer,
        "update": ReplyUpdateSerializer,
    }
    http_method_names = ('get', 'post', 'put', 'delete')
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('on_post', )

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ReplyListSerializer)


class FavoriteViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Favorite.objects.all()
    serializer_classes = {
        "update": FavoriteUpdateSerializer,
    }
    http_method_names = ('get', 'post', 'put')

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, FavoriteSerializer)
