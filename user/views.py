from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import status
from main.responses import format_api_response
from .serializers import ProfileSerializer, PasswordUpdateSerializer
from .models import CustomUser
from .messages import (
    OLD_PASSWORD_INCORRECT,
    PASSWORD_UPDATE_SUCCESS,
    PROFILE_UPDATE_SUCCESS

)


class Password(APIView):
    serializer_class = PasswordUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Update user password
        """
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


password = Password.as_view()


class Profile(APIView):

    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Read user profile
        """
        user = request.user
        serializer = self.get_serializer(user)
        api_response = format_api_response(content=serializer.data)
        return Response(api_response, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        Partial update user profile
        """
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        api_response = format_api_response(
            content=serializer.data, message=PROFILE_UPDATE_SUCCESS
        )
        return Response(api_response, status=status.HTTP_200_OK)


profile = Profile.as_view()
