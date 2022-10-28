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
    register_confirmation_body,
)
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from main.responses import format_api_response
from .messages import (
    LOGIN_SUCCESS,
    LOGOUT_SUCCESS,
    REGISTER_SUCCESS,
    EMAIL_CONFIRMATION_REQUIRED,
    EMAIL_CONFIRMATION_DONE,
    EMAIL_CONFIRMATION_ALREADY_DONE,
    OLD_PASSWORD_INCORRECT,
    PASSWORD_UPDATE_SUCCESS,
    PASSWORD_RESET_LINK_SENT,
    TOKEN_ALREADY_USED,
    MISC_ERROR,
)

from main.settings import EMAIL_VALIDATION_URL, PASSWORD_RESET_URL


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        if not user.email_validated:
            api_response = format_api_response(
                status=401, message=EMAIL_CONFIRMATION_REQUIRED, error=True
            )
            return Response(api_response)

        token, created = Token.objects.get_or_create(user=user)
        api_response = format_api_response(
            content={"token": token.key}, message=LOGIN_SUCCESS
        )
        return Response(api_response, status=200)


login = Login.as_view()


class Logout(APIView):
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()

        api_response = format_api_response(message=LOGOUT_SUCCESS)
        return Response(api_response, status=200)


logout = Logout.as_view()


class Register(APIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get_email_confirmation_link(self, user):
        email_token = EmailValidationToken.objects.create(user=user)
        return f"{EMAIL_VALIDATION_URL}{email_token}"

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            password = request.data["password"]
            validate_password(password)
        except ValidationError as e:
            api_response = format_api_response(
                content={"password": e}, status=401, error=True, message=MISC_ERROR
            )
            return Response(api_response, status=401)

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
        api_response = format_api_response(message=REGISTER_SUCCESS)

        return Response(api_response, status=200)


register = Register.as_view()


class EmailValidation(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):

        key = kwargs.get("key")
        validation_token = get_object_or_404(EmailValidationToken, key=key)

        if validation_token.is_used:
            api_response = format_api_response(
                message=EMAIL_CONFIRMATION_ALREADY_DONE, status=401
            )
            return Response(api_response, status=401)

        validation_token.user.email_validated = True
        validation_token.is_used = True
        validation_token.save()
        validation_token.user.save()

        api_response = format_api_response(message=EMAIL_CONFIRMATION_DONE)

        return Response(api_response, status=200)


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

        if not user.check_password(old_password):
            api_response = format_api_response(
                message=OLD_PASSWORD_INCORRECT, status=401
            )
            return Response(api_response, status=401)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            api_response = format_api_response(
                content={"password": e}, status=401, error=True, message=MISC_ERROR
            )
            return Response(api_response, status=401)

        user.set_password(new_password)
        user.save()

        api_reponse = format_api_response(message=PASSWORD_UPDATE_SUCCESS)
        return Response(api_reponse, status=200)


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
            if user.email_validated:
                (
                    validation_token,
                    created,
                ) = PasswordValidationToken.objects.get_or_create(user=user)
                print("PASSWORD TOKEN:", validation_token)

                # send_mail(
                #     f"Welcome {user.username}",
                #     register_confirmation_email(user.username, "XXXXX"),
                #     "noreply@APP_NAME.com",
                #     [user.email],
                #     fail_silently=False,
                # )

        api_response = format_api_response(message=PASSWORD_RESET_LINK_SENT)
        return Response(api_response, status=200)


password_forget = PasswordForget.as_view()


class PasswordReset(APIView):
    serializer_class = PasswordResetSerializer
    permission_classes = []

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        key = kwargs.get("key")
        validation_token = get_object_or_404(PasswordValidationToken, key=key)
        user = validation_token.user
        if validation_token.is_used:
            api_response = format_api_response(
                message=TOKEN_ALREADY_USED, status=401, error=True
            )
            return Response(api_response, status=401)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data["password"]

        try:
            validate_password(password, user)
        except ValidationError as e:
            return Response({"detail": e})

        user.set_password(password)
        user.save()
        validation_token.is_used = True
        validation_token.save()

        api_response = format_api_response(message=PASSWORD_UPDATE_SUCCESS)
        return Response(api_response, status=200)


password_reset = PasswordReset.as_view()
