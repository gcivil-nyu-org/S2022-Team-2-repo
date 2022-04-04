from django.contrib.auth.models import User
from django.test import TestCase

from .forms import UserRegisterForm, ResetPasswordRequestForm, PreferencesExploreForm
from .tokens import TokenGenerator, account_activation_token


class SignupFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dummy_user_wrong = {
            "username": "testname",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "test1234",
            "password2": "test1234",
        }
        cls.dummy_user_right = {
            "username": "ts4044",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "django1234",
            "password2": "django1234",
        }

    def test_pass_normal(self):
        form = UserRegisterForm(data=self.dummy_user_right)
        self.assertFalse(form.errors)

    def test_fail_username(self):
        form = UserRegisterForm(data=self.dummy_user_wrong)
        self.assertTrue(form.errors)


class ResetPasswordRequestFormTest(TestCase):
    def test_pass_normal(self):
        form = ResetPasswordRequestForm(data={"username": "ts4044"})
        self.assertFalse(form.errors)


class PreferencesExploreFormTest(TestCase):
    def test_pass(self):
        form = PreferencesExploreForm(
            data={
                "food_choices": ["NI"],
                "travel_choices": ["NI"],
                "sports_choices": ["NI"],
                "nyc_choices": ["NI"],
                "pet_choices": ["NI"],
            }
        )
        self.assertFalse(form.errors)


class TestCalls(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User._default_manager.create_user(
            username="test012",
            email="test012@nyu.edu",
            password="django1234",
            first_name="John",
            last_name="Doe",
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get("/dashboard/", follow=True)
        self.assertRedirects(response, "/login/?next=/dashboard/")

    def test_call_view_fail_blank(self):
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()
        logged_in = self.client.login(username="testuser", password="12345")
        self.assertTrue(logged_in)


class TestTokenGenerator(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User._default_manager.create_user(
            username="test012",
            email="test012@nyu.edu",
            password="django1234",
            first_name="John",
            last_name="Doe",
        )

    def token_generator_test(self):
        hash_val1 = account_activation_token.make_token(self.user)
        self.assertTrue(hash_val1)
        hash_val = TokenGenerator._make_hash_value("user", "testpassword")
        self.assertTrue(hash_val)
