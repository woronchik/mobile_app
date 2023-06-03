from celery import shared_task
from django.contrib.auth import get_user_model

from users.models import EmailConfirmationCode, ResetPasswordToken
from users.services.email_service import EmailNotificationService


@shared_task
def send_recovery_code(user_id):
    print(f"Sending email to user {user_id}...")
    user = get_user_model().objects.filter(id=user_id).first()

    if not user:
        print(f"User with id {user_id} not found")

    EmailConfirmationCode.objects.filter(email=user.email).delete()
    ResetPasswordToken.objects.filter(user=user).delete()

    recovery_code = EmailConfirmationCode.objects.create(email=user.email)

    email_body = f"Hello, here is your recovery code: {recovery_code}"

    EmailNotificationService.send_email(subject='Recovery code', body=email_body, to_email=[user.email, ])
