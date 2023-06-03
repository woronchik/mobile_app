from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

from users.celery_tasks import send_recovery_code
from users.models import ResetPasswordToken, EmailConfirmationCode


class RecoveryService:
    @staticmethod
    def get_user(email):
        user = get_user_model().objects.filter(email=email).first()
        if not user:
            raise NotFound(detail=f"User with email {email} not found")
        return user

    @classmethod
    def send_recovery_code_message(cls, target_email):
        user = cls.get_user(target_email)
        send_recovery_code.delay(user.id)

    @classmethod
    def get_token_for_password(cls, email):
        EmailConfirmationCode.objects.filter(email=email).delete()
        user = cls.get_user(email=email)
        return ResetPasswordToken.objects.create(user=user).token

    @classmethod
    def reset_password(cls, email, new_password, token):
        user = cls.get_user(email=email)
        token = ResetPasswordToken.objects.filter(token=token, user=user).first()

        if not token:
            raise NotFound(detail="there is no such token for this email")

        user.set_password(new_password)
        user.save()
        token.delete()

