from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser
from authentication.models import (
    EmailValidationToken,
    AuthToken,
    PasswordValidationToken,
)


class AuthenticationTests(APITestCase):

    user_id = 1
    username = "Testing"
    email = "testingApp@mail.com"
    password = "TestingTesting"
    auth_token = "auth69875ecdaa628405940f83a3ba6f3a466718"
    email_validation_token = "email9875ecdaa628405940f83a3ba6f3a466718"
    password_reset_token = "password5ecdaa628405940f83a3ba6f3a466718"

    @classmethod
    def setUpClass(cls):
        user = CustomUser.objects.create_user(
            username=cls.username,
            email=cls.email,
            password=cls.password,
            email_validated=True,
        )

        AuthToken.objects.create(user=user, key=cls.auth_token)
        EmailValidationToken.objects.create(user=user, key=cls.email_validation_token)
        PasswordValidationToken.objects.create(user=user, key=cls.password_reset_token)

        super().setUpClass()

    # def test_register(self):
    #     """
    #     Ensure we can create a new account object.
    #     """
    #     url = reverse("api_register")
    #     data = {
    #         "username": "RegisterExample",
    #         "email": "email_example@mail.com",
    #         "password": "ARandomPassword",
    #     }
    #     response = self.client.post(url, data, format="json")

    #     self.assertEqual(EmailValidationToken.objects.count(), 1)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(
    #         CustomUser.objects.get(email=data["email"]).username,
    #         data["username"],
    #     )

    def test_email_validation(self):
        """
        Ensure we can confirm email with provided token
        """

        url = reverse(
            "api_email_validation", kwargs={"key": self.email_validation_token}
        )
        response = self.client.get(url, format="json")
        user = CustomUser.objects.get(id=self.user_id)
        email_token = EmailValidationToken.objects.get(key=self.email_validation_token)

        self.assertEqual(email_token.is_used, 1)
        self.assertEqual(user.email_validated, 1)

    def test_login(self):
        """
        Ensure we can login with credentials and obtain a token
        """
        url = reverse("api_login")

        data = {"username": self.email, "password": self.password}
        response = self.client.post(
            url,
            data,
            format="json",
        )
        user = CustomUser.objects.get(id=self.user_id)
        response_token = response.data["body"]["token"]
        user_token = AuthToken.objects.get(user=user).key

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_token, user_token)

    def test_logout(self):
        """
        Ensure we can logout and remove user auth token
        """

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        url = reverse("api_logout")
        response = self.client.post(
            url,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AuthToken.objects.count(), 0)
