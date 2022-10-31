from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Default user model
    """

    RUE = "rue"
    BOULEVARD = "boulevard"
    IMPASSE = "impasse"
    CHEMIN = "chemin"
    LIEU_DIT = "lieu dit"

    STREET_TYPES_CHOICES = [
        (RUE, "rue"),
        (BOULEVARD, "boulevard"),
        (IMPASSE, "impasse"),
        (CHEMIN, "chemin"),
        (LIEU_DIT, "lieu dit"),
    ]

    username = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    email_validated = models.BooleanField(default=False)

    date_of_birth = models.DateField(blank=True, null=True)

    street_number = models.CharField(max_length=10, blank=True)
    street_type = models.CharField(
        max_length=50, choices=STREET_TYPES_CHOICES, blank=True
    )
    street_name = models.CharField(max_length=200, blank=True)
    city_zipcode = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    phone_number = models.CharField(max_length=15, blank=True)
    phone_validated = models.BooleanField(default=False)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
