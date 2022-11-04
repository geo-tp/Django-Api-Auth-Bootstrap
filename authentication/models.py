import binascii
import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser
from rest_framework.authtoken.models import Token


class CustomToken(models.Model):
    """
    The default token model for non auth usage
    """

    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(CustomToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class AuthToken(Token):
    """
    Token for authenticate user, the one returned when succesfull login
    """

    pass


class EmailValidationToken(CustomToken):
    """
    Token sended to user email during user registration process
    """

    pass


class PasswordValidationToken(CustomToken):
    """
    Token sended to user email during password reset process
    """

    pass
