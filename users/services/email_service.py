from django.core.mail import EmailMessage


class EmailNotificationService:
    @staticmethod
    def send_email(subject, body, to_email):
        email = EmailMessage(subject=subject, body=body, to=to_email)
        email.send()
