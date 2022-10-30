from rest_framework import serializers
from .models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "street_number",
            "street_type",
            "street_name",
            "city_number",
            "city",
            "phone_number",
        ]
        read_only_fields = ["username", "email"]


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
