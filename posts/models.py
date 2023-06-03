from django.db import models

from users.models import ProfileType, UserProfile, CustomUser


class GenderEnum(models.TextChoices):
    MALE = "male"
    FEMALE = "female"
    ALL = "all"

class AcceptanceStatusEnum(models.TextChoices):
    ACCEPTED = "accepted"
    DECLINED = "declined"
    PENDING = "pending"


class Post(models.Model):
    #PHOTO
    photo = models.FileField(upload_to='posts/photos/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    execution_date = models.DateTimeField(null=True)
    budget = models.PositiveIntegerField(null=True)
    city = models.CharField(max_length=100, null=True)
    performer_gender = models.CharField(max_length=10, choices=GenderEnum.choices, default=GenderEnum.ALL)
    age_from = models.IntegerField(null=True)
    age_to = models.IntegerField(null=True)
    height_from = models.IntegerField(null=True)
    height_to = models.IntegerField(null=True)
    has_international_passport = models.BooleanField(default=False)
    has_tatoo_or_piercing = models.BooleanField(default=False)
    other_details = models.TextField(max_length=255, blank=True, null=True)
    profile_type = models.CharField(max_length=25, choices=ProfileType.choices, default=ProfileType.MODEL)

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Reply(models.Model):
    from_person = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    acceptance_status = models.CharField(
        max_length=50,
        choices=AcceptanceStatusEnum.choices,
        default=AcceptanceStatusEnum.PENDING
    )


class Favorite(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    favorite_posts = models.ManyToManyField(Post)
    favorite_models = models.ManyToManyField(UserProfile)

    class Meta:
        db_table = 'favorites'
