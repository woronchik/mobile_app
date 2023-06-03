from django.utils import timezone
from rest_framework import serializers

from users.models import CustomUser, UserProfile, EmailConfirmationCode, ResetPasswordToken


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "role"
        )


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "password")
        read_only_fields = ("id",)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("password",)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ("id",)


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "user_photo", "name", "city")


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class CheckCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmationCode
        fields = ('email', 'recovery_code')

    def validate(self, data):
        notification = EmailConfirmationCode.objects.filter(email=data['email'],
                                                            recovery_code=data['recovery_code']).first()
        if notification.expire_at < timezone.now():
            raise serializers.ValidationError("Code already expired")
        elif notification.recovery_code != data['recovery_code']:
            raise serializers.ValidationError("Code is not the same")

        return data


class UpdatePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    temporary_token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        token = ResetPasswordToken.objects.filter(token=data['temporary_token']).first()
        if not token:
            raise serializers.ValidationError("there is no such token")
        elif token.expire_at < timezone.now():
            raise serializers.ValidationError("Code already expired")
        return data
