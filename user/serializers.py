import re
from datetime import date
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import CustomUser
from .messages import (
    PHONE_FORMAT_INCORRECT,
    ZIPCODE_FORMAT_INCORRECT,
    CITY_FORMAT_INCORRECT,
    LAST_NAME_FORMAT_INCORRECT,
    FIRST_NAME_FORMAT_INCORRECT,
    STREET_NAME_FORMAT_INCORRECT,
    BIRTH_DATE_FORMAT_INCORRECT,
)
from main.regexp import (
    french_city_zipcode_regexp_pattern,
    french_phone_regexp_pattern,
    name_regexp_pattern,
)


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
            "city_zipcode",
            "city",
            "address_complement",
            "country",
            "phone_number",
        ]
        read_only_fields = ["username", "email"]

    def validate_phone_number(self, value):

        # French phone validation
        regexp_pattern = french_phone_regexp_pattern

        if re.search(regexp_pattern, value):
            return value

        raise serializers.ValidationError([PHONE_FORMAT_INCORRECT])

    def validate_city_zipcode(self, value):

        # French city zipcode
        regexp_pattern = french_city_zipcode_regexp_pattern

        if re.search(regexp_pattern, value):
            return value

        raise serializers.ValidationError([ZIPCODE_FORMAT_INCORRECT])

    def validate_city(self, value):

        regexp_pattern = name_regexp_pattern

        if re.search(regexp_pattern, value):
            return value

        raise serializers.ValidationError([CITY_FORMAT_INCORRECT])

    def validate_country(self, value):

        regexp_pattern = name_regexp_pattern

        if re.search(regexp_pattern, value):
            return value

        raise serializers.ValidationError([COUNTRY_FORMAT_INCORRECT])

    def validate_street_name(self, value):

        regexp_pattern = name_regexp_pattern

        if re.search(regexp_pattern, value):
            return value

        raise serializers.ValidationError([STREET_NAME_FORMAT_INCORRECT])

    def validate_first_name(self, value):

        regexp_pattern = name_regexp_pattern

        if re.search(regexp_pattern, value):
            return value

        raise serializers.ValidationError([FIRST_NAME_FORMAT_INCORRECT])

    def validate_last_name(self, value):

        regexp_pattern = name_regexp_pattern

        if re.search(regexp_pattern, value):
            return value

        raise serializers.ValidationError([LAST_NAME_FORMAT_INCORRECT])

    def validate_date_of_birth(self, value):

        oldest_accepted_birth_date = date(
            date.today().year - 120,
            date.today().month,
            date.today().day,
        )

        if value < date.today() and value > oldest_accepted_birth_date:
            return value

        raise serializers.ValidationError([BIRTH_DATE_FORMAT_INCORRECT])


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    def validate_new_password(self, value):
        validate_password(value, CustomUser)
        return value
