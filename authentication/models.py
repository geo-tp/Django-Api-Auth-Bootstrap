# import binascii
# import os

# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from user.models import CustomUser

# class CustomToken(models.Model):
#     """
#     The default authorization token model.
#     """
#     key = models.CharField(_("Key"), max_length=40, primary_key=True)

#     user = models.OneToOneField(
#         CustomUser, related_name='auth_custom_token',
#         on_delete=models.CASCADE, verbose_name="user"
#     )
#     created = models.DateTimeField(_("Created"), auto_now_add=True)

#     class Meta:
#         verbose_name = _("Token")
#         verbose_name_plural = _("Tokens")

#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super(CustomToken, self).save(*args, **kwargs)

#     def generate_key(self):
#         return binascii.hexlify(os.urandom(20)).decode()

#     def __str__(self):
#         return self.key
