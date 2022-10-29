from django.shortcuts import render
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from main.responses import format_api_response
from rest_framework.decorators import action
from .messages import PROFILE_UPDATE_SUCCESS
from .models import CustomUser
from rest_framework import permissions
from rest_framework import status


class UserViewSet(viewsets.GenericViewSet):
    """
    User Authenticated views
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def profile(self, request, *args, **kwargs):
        """
        Read user profile
        """
        user = request.user
        serializer = self.get_serializer(user)
        api_response = format_api_response(content=serializer.data)
        return Response(api_response, status=status.HTTP_200_OK)

    @profile.mapping.put
    @profile.mapping.patch
    def update_profile(self, request, *args, **kwargs):
        """
        Update user profile
        """
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        api_response = format_api_response(
            content=serializer.data, message=PROFILE_UPDATE_SUCCESS
        )
        return Response(api_response, status=status.HTTP_200_OK)
