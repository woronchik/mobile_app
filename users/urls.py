from rest_framework import routers

from users.views import UserViewSet, ProfileViewSet, PasswordResetViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register(r"customuser", UserViewSet, basename="customuser")
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"password-reset", PasswordResetViewSet, basename="password-reset")

urlpatterns = router.urls
