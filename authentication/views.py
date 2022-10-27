from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.authtoken.models import Token

class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

login = Login.as_view()

class Logout(APIView):

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()

        return Response('User Logged out successfully')

logout = Logout.as_view()

class Register(APIView):
    serializer_class = RegisterSerializer
    permission_classes = []


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })

register = Register.as_view()
