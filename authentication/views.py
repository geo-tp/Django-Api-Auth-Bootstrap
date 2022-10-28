from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import (
    RegisterSerializer,
    PasswordUpdateSerializer,
    PasswordResetSerializer,
    PasswordForgetSerializer,
)
from rest_framework.authtoken.models import Token
from .models import EmailValidationToken, PasswordValidationToken
from user.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from authentication.emails import (
    register_confirmation_email,
)
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        if not user.email_validated:
            return Response({"detail": "You need to confirm your email"})

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


login = Login.as_view()


class Logout(APIView):
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()

        return Response("User Logged out successfully")


logout = Logout.as_view()


class Register(APIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get_email_confirmation_link(self, user):
        email_token = EmailValidationToken.objects.create(user=user)
        return f"http://localhost:8000/{email_token}"

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_link = self.get_email_confirmation_link(user)
        print("CONFIRMATION LINK :", confirmation_link)

        # send_mail(
        #     f"Welcome {user.username}",
        #     register_confirmation_email(user.username, "XXXXX"),
        #     "noreply@APP_NAME.com",
        #     [user.email],
        #     fail_silently=False,
        # )

        return Response(
            {"detail": "Successfully registered, you will receive an email"}
        )


register = Register.as_view()


class EmailValidation(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):

        key = kwargs.get("key")
        validation_token = get_object_or_404(EmailValidationToken, key=key)

        if validation_token.is_used:
            return Response({"detail": "Email is already confirmed"})

        validation_token.user.email_validated = True
        validation_token.is_used = True
        validation_token.save()
        validation_token.user.save()

        return Response({"detail": "Email confirmation is done, you can login now"})


email_validation = EmailValidation.as_view()


class PasswordUpdate(APIView):
    serializer_class = PasswordUpdateSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.data["old_password"]
        new_password = serializer.data["new_password"]
        user = request.user
        print(user.check_password(old_password))

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect"})

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"detail": e})

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password Updated successfully"})


password_update = PasswordUpdate.as_view()


class PasswordForget(APIView):
    serializer_class = PasswordForgetSerializer
    permission_classes = []

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]

        try:
            user = CustomUser.objects.get(email=email)
        except:
            user = None

        if user:
            validation_token = PasswordValidationToken.objects.create(user)
            print("PASSWORD TOKEN:", validation_token.key)

            # send_mail(
            #     f"Welcome {user.username}",
            #     register_confirmation_email(user.username, "XXXXX"),
            #     "noreply@APP_NAME.com",
            #     [user.email],
            #     fail_silently=False,
            # )

        return Response({"detail": "Check reset link in your mailbox"})


password_forget = PasswordForget.as_view()


class PasswordReset(APIView):
    serializer_class = PasswordForgetSerializer
    permission_classes = []

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data["password"]

        try:
            validate_password(password, user)
        except ValidationError as e:
            return Response({"detail": e})

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password Reset successfully"})


password_reset = PasswordReset.as_view()
