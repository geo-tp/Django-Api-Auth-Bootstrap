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
from rest_framework import status
from .models import EmailValidationToken, PasswordValidationToken
from user.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from authentication.emails import (
    send_register_confirmation_email,
    send_password_reset_email
)
from django.shortcuts import get_object_or_404
from rest_framework import permissions
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
    ACCOUNT_DEACTIVATED,
)

from main.settings import EMAIL_VALIDATION_URL, PASSWORD_RESET_URL, EMAIL_HOST_USER


class Login(ObtainAuthToken):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Login user with username/pwd or email/pwd
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        if not user.email_validated or user.is_active:
            api_response = format_api_response(
                status=status.HTTP_400_BAD_REQUEST,
                message=EMAIL_CONFIRMATION_REQUIRED,
                error=True,
            )
            return Response(api_response, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            api_response = format_api_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message=ACCOUNT_DEACTIVATED,
                error=True,
            )
            return Response(api_response, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        api_response = format_api_response(
            content={"token": token.key}, message=LOGIN_SUCCESS
        )
        return Response(api_response, status=status.HTTP_200_OK)


login = Login.as_view()


class Logout(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Logout a user by removing its auth token
        """
        request.user.auth_token.delete()

        api_response = format_api_response(message=LOGOUT_SUCCESS)
        return Response(api_response, status=status.HTTP_200_OK)


logout = Logout.as_view()


class Register(APIView):
    """
    Register a new user
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            password = request.data["password"]
            validate_password(password)
        except ValidationError as e:
            api_response = format_api_response(
                content={"password": e},
                status=status.HTTP_400_BAD_REQUEST,
                error=True,
                message=MISC_ERROR,
            )
            return Response(api_response, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        email_token = EmailValidationToken.objects.create(user=user)

        send_register_confirmation_email(
            user.email, user.username, email_token)
        api_response = format_api_response(message=REGISTER_SUCCESS)

        return Response(api_response, status=status.HTTP_200_OK)


register = Register.as_view()


class EmailValidation(APIView):
    """
    Validate email with received token
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        key = kwargs.get("key")
        validation_token = get_object_or_404(EmailValidationToken, key=key)

        if validation_token.is_used:
            api_response = format_api_response(
                message=EMAIL_CONFIRMATION_ALREADY_DONE,
                status=status.HTTP_400_BAD_REQUEST,
            )
            return Response(api_response, status=status.HTTP_400_BAD_REQUEST)

        validation_token.user.email_validated = True
        validation_token.is_used = True
        validation_token.save()
        validation_token.user.save()

        api_response = format_api_response(message=EMAIL_CONFIRMATION_DONE)

        return Response(api_response, status=status.HTTP_200_OK)


email_validation = EmailValidation.as_view()


class PasswordUpdate(APIView):
    """
    Update user password
    """
    serializer_class = PasswordUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

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
                message=OLD_PASSWORD_INCORRECT, status=status.HTTP_400_BAD_REQUEST
            )
            return Response(api_response, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            api_response = format_api_response(
                content={"password": e},
                status=status.HTTP_400_BAD_REQUEST,
                error=True,
                message=MISC_ERROR,
            )
            return Response(api_response, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        api_reponse = format_api_response(message=PASSWORD_UPDATE_SUCCESS)
        return Response(api_reponse, status=status.HTTP_200_OK)


password_update = PasswordUpdate.as_view()


class PasswordForget(APIView):
    """
    Send a link to reset password by mail when a correct email address is provided
    """
    serializer_class = PasswordForgetSerializer
    permission_classes = [permissions.AllowAny]

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
                    password_token,
                    created,
                ) = PasswordValidationToken.objects.get_or_create(user=user)
                print("PASSWORD TOKEN:", validation_token)

                send_password_reset_email(
                    user.email, user.username, password_token)
        api_response = format_api_response(message=PASSWORD_RESET_LINK_SENT)
        return Response(api_response, status=status.HTTP_200_OK)


password_forget = PasswordForget.as_view()


class PasswordReset(APIView):
    """
    Reset user password with the one provided (requires password reset token)
    """
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        key = kwargs.get("key")
        validation_token = get_object_or_404(PasswordValidationToken, key=key)
        user = validation_token.user
        if validation_token.is_used:
            api_response = format_api_response(
                message=TOKEN_ALREADY_USED,
                status=status.HTTP_400_BAD_REQUEST,
                error=True,
            )
            return Response(api_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data["password"]

        try:
            validate_password(password)
        except ValidationError as e:
            api_response = format_api_response(
                content={"password": e},
                status=status.HTTP_400_BAD_REQUEST,
                error=True,
                message=MISC_ERROR,
            )
            return Response(api_response, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        validation_token.is_used = True
        validation_token.save()

        api_response = format_api_response(message=PASSWORD_UPDATE_SUCCESS)
        return Response(api_response, status=status.HTTP_200_OK)


password_reset = PasswordReset.as_view()


class DeactivateAccount(APIView):
    """
    Deactivate user account, user will be disconnected and not able to connect anymore
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        auth_token = Token.objects.get(user=user)
        auth_token.delete()
        user.is_active = False
        user.save()

        api_response = format_api_response(message=ACCOUNT_DEACTIVATED)
        return Response(api_response, status=status.HTTP_200_OK)


deactivate_account = DeactivateAccount().as_view()
