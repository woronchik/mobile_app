from django.contrib.auth.models import AbstractUser
from django.db import models

from users.services.token_service import TokenService


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin"
        USER = "user"

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length=15, choices=Roles.choices, default=Roles.USER)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email


class Gender(models.IntegerChoices):
    MALE = 0
    FEMALE = 1


class ProfileType(models.TextChoices):
    MODEL = "model"
    PHOTOGRAPHER = "photographer"
    AGENCY = "agency"


class UserProfile(models.Model):
    user_photo = models.FileField(upload_to='users/photos/', null=True, blank=True)
    name = models.CharField(max_length=25, blank=False, null=False)
    profile_type = models.CharField(max_length=25, choices=ProfileType.choices, default=ProfileType.MODEL)
    gender = models.IntegerField(choices=Gender.choices, default=Gender.MALE)
    has_international_passport = models.BooleanField(default=False)
    has_tatoo_or_piercing = models.BooleanField(default=False)
    age = models.IntegerField(null=True)
    city = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=20, null=True)
    instagram = models.CharField(max_length=150, null=True, blank=True)
    facebook = models.CharField(max_length=150, null=True, blank=True)
    linkedin = models.CharField(max_length=150, null=True, blank=True)
    website = models.CharField(max_length=150, null=True, blank=True)
    clothes_size = models.IntegerField(null=True, blank=True)
    shoes_size = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    bust = models.IntegerField(null=True, blank=True)
    waist = models.IntegerField(null=True, blank=True)
    hips = models.IntegerField(null=True, blank=True)
    look_type = models.CharField(max_length=100, null=True, blank=True)
    skin_color = models.CharField(max_length=100, null=True, blank=True)
    hair_color = models.CharField(max_length=100, null=True, blank=True)
    hair_length = models.IntegerField(null=True, blank=True)
    known_languages = models.CharField(max_length=150, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, db_column='user_id')

    class Meta:
        db_table = "profile"


class ResetPasswordToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    token = models.CharField(default=TokenService.generate_token, max_length=100, null=True)
    expire_at = models.DateTimeField(default=TokenService.generate_expire, null=True)

    class Meta:
        db_table = "reset_password"


class EmailConfirmationCode(models.Model):
    email = models.EmailField()
    recovery_code = models.IntegerField(default=TokenService.generate_code, null=True)
    expire_at = models.DateTimeField(default=TokenService.generate_expire, null=True)

    class Meta:
        db_table = "email_confirmation"
