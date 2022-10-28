from django.shortcuts import render
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework import viewsets, mixins
from rest_framework.views import APIView


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):

    # http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']
    permission_classes = []

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
