from rest_framework import serializers
from user.models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "date_of_birth",
            "street_number",
            "street_type",
            "street_name",
            "city_number",
            "city",
            "phone_number",
        ]

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",

        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])