from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser, UserProfileImage
from authentication.models import (
    EmailValidationToken,
    AuthToken,
    PasswordValidationToken,
)
from generic.models import GenericImage
from generic.tests import APITestCaseWithUser


class UserTests(APITestCaseWithUser):
    """
    Tests for each Authentication view
    """

    # user_id = 1
    # auth_token = "auth69875ecdaa628405940f83a3ba6f3a466718"
    # email_validation_token = "email9875ecdaa628405940f83a3ba6f3a466718"

    def test_profile_update(self):
        """
        Ensure we can update user profile
        """

        url = reverse("api_user_profile")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "city": "Paris",
            "phone_number": "0606060606",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.patch(url, data, format="json")
        user = CustomUser.objects.get(email=self.email)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["first_name"], user.first_name)

    def test_password_update(self):
        """
        Ensure we can update user password
        """
        pass
