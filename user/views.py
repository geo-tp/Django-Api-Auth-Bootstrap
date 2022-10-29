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


class UserViewSet(viewsets.GenericViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def profile(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        api_response = format_api_response(content=serializer.data)
        return Response(api_response, status=200)

    @profile.mapping.put
    @profile.mapping.patch
    def update_profile(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        api_response = format_api_response(
            content=serializer.data, message=PROFILE_UPDATE_SUCCESS
        )
        return Response(api_response, status=200)
