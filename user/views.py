from django.shortcuts import render
from .serializers import UserSerializer, DetailledUserSerializer
from .models import CustomUser
from rest_framework import viewsets
import django_filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from ebay_base.functions_utils import checkUserMatching, checkUserIsOwner,\
                             checkSenderIsNotReceiver, restrictedEndPoint, checkUserIsReceiver
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):

    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["username", "email"]


    permission_classes = [IsAuthenticatedOrReadOnly]


# class DetailledUserViewSet(viewsets.ModelViewSet):

#     http_method_names = ["get"]

#     queryset = CustomUser.objects.all()
#     serializer_class = DetailledUserSerializer

#     @checkUserIsOwner
#     @method_decorator(cache_page(60))
#     def retrieve(self, request, pk):
        
#         return super().retrieve(request, pk)

#     @restrictedEndPoint
#     def list(self, request):
#             pass     

