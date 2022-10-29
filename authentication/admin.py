from django.contrib import admin
from .models import EmailValidationToken, PasswordValidationToken

# Register your models here.
admin.site.register(EmailValidationToken)
admin.site.register(PasswordValidationToken)
