from rest_framework import serializers

from users.models import CustomUser

from rest_framework import serializers
from rest_auth.models import TokenModel
from rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser

from ebay_base.functions_utils import hidePartOfPaymentMethod
# from rest_auth.utils import import_callable

class BasicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class CustomRegisterSerializer(RegisterSerializer):

    last_name = serializers.CharField()
    first_name = serializers.CharField()
    date_of_birth = serializers.DateField()

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.date_of_birth = self.validated_data.get('date_of_birth', '')

        user.save(update_fields=['first_name', 'last_name', 'date_of_birth'])


class ExpeditionUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth',
                  "street_number", "street_type", "street_name", "city_number", "city"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id',"username", 'email', 'first_name', 'last_name', 'date_of_birth',
                  "street_number", "street_type", "street_name", "city_number", "city", "phone_number"]


class CustomTokenSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', 'user', )

class DetailledUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ("password", )


    def to_representation(self, instance):

        rep = super().to_representation(instance)

        rep["card_number"] = hidePartOfPaymentMethod(rep["card_number"])
        rep["iban"] = hidePartOfPaymentMethod(rep["iban"])
        
        return rep