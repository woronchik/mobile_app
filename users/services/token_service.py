import random
import string

from django.utils import timezone


class TokenService:
    @staticmethod
    def generate_token():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(60))

    @staticmethod
    def generate_code():
        return random.randint(1000, 9999)

    @staticmethod
    def generate_expire():
        return timezone.now() + timezone.timedelta(minutes=5)
