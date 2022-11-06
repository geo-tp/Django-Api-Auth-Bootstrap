from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from main import settings


class CustomUser(AbstractUser):
    """
    Default user model
    """

    username = models.CharField(max_length=50, unique=True, blank=True)

    birthdate = models.DateField(blank=True, null=True)

    street_number = models.CharField(max_length=20, blank=True)
    street_type = models.CharField(max_length=50, blank=True)
    street_name = models.CharField(max_length=200, blank=True)
    city_zipcode = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=200, blank=True)
    address_complement = models.CharField(max_length=500, blank=True)
    country = models.CharField(max_length=200, blank=True, default="France")

    email = models.EmailField(_("email address"), unique=True)
    email_validated = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=15, blank=True)
    phone_validated = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserProfileImage(models.Model):
    image = models.ForeignKey("generic.GenericImage", on_delete=models.CASCADE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile_image",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
