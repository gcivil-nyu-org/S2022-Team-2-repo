from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

dummy_user_right = {
    "username": "test1234",
    "email": "test1234@nyu.edu",
    "first_name": "John",
    "last_name": "Doe",
    "password": "Crypt1234",
}


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_call_view_deny_anonymous(self):
        response = self.client.get("/dashboard/", follow=True)
        self.assertRedirects(response, "/login/?next=/dashboard/")

    def test_call_view_fail_blank(self):
        self.user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )
        response = self.client.post(
            "/login/",
            {
                "username": dummy_user_right["username"],
                "password": dummy_user_right["password"],
            },
            follow=True,
        )
        self.assertEquals(response.status_code, 200)


class LogoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get("/logout/", follow=True)
        self.assertRedirects(response, "/login/?next=/logout/")

    def test_redirect_successful_logout(self):
        self.client.force_login(user=self.user)
        response = self.client.get("/logout/", follow=True)
        self.assertRedirects(response, "/")


class ProfileSetupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("profile_setup"), follow=True)
        self.assertRedirects(response, "/login/?next=/profile/setup")
