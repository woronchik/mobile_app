from rest_framework import routers

from posts.views import PostViewSet, ReplyViewSet, FavoriteViewSet

app_name = "posts"

router = routers.DefaultRouter()
router.register(r"post", PostViewSet, basename="posts")
router.register(r"reply", ReplyViewSet, basename="reply")
router.register(r"favorite", FavoriteViewSet, basename="favorite")

urlpatterns = router.urls
