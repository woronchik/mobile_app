from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from users.models import CustomUser, UserProfile, ResetPasswordToken
from users.serializers import UserUpdateSerializer, UserCreateSerializer, UserGetSerializer, ProfileSerializer, \
    ProfileListSerializer, ResetPasswordEmailSerializer, CheckCodeSerializer, UpdatePasswordSerializer
from users.services.recovery_service import RecoveryService


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = CustomUser.objects.all()
    serializer_classes = {
        "create": UserCreateSerializer,
        "partial_update": UserUpdateSerializer,
    }
    http_method_names = ('get', 'patch', 'delete', 'post')

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, UserGetSerializer)


class ProfileViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = UserProfile.objects.all()
    serializer_classes = {
        "list": ProfileListSerializer
    }
    http_method_names = ('post', 'get', 'patch', 'delete')
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ProfileSerializer)


class PasswordResetViewSet(
    viewsets.GenericViewSet
):
    serializer_class = ResetPasswordEmailSerializer
    queryset = ResetPasswordToken.objects.all()

    @action(detail=False, methods=('POST',), url_path='send-reset-email', serializer_class=ResetPasswordEmailSerializer)
    def send_reset_email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        RecoveryService.send_recovery_code_message(target_email=email)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('POST',), url_path='check-recovery-code', serializer_class=CheckCodeSerializer)
    def check_recovery_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        token = RecoveryService.get_token_for_password(email=email)
        return Response(data={'temporary_token': token}, status=status.HTTP_200_OK)

    @action(detail=False, methods=('POST',), url_path='create-new-password', serializer_class=UpdatePasswordSerializer)
    def create_new_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email, new_password, token = serializer.validated_data['email'], serializer.validated_data['password'], serializer.validated_data['temporary_token']

        RecoveryService.reset_password(email=email, new_password=new_password, token=token)
        return Response(data={'message': "Password has been successfully changed"}, status=status.HTTP_200_OK)
