from unittest import TestCase

from users.forms import (
    UserRegisterForm,
    ResetPasswordRequestForm,
    PreferencesExploreForm,
)

dummy_user_right = {
    "username": "test1234",
    "first_name": "John",
    "last_name": "Doe",
    "password1": "Crypt1234",
    "password2": "Crypt1234",
}
dummy_user_wrong = {
    "username": "wrong_username",
    "first_name": "John",
    "last_name": "Doe",
    "password1": "Crypt1234",
    "password2": "Crypt1234",
}
password_wrong = {
    "username": "test1234",
    "first_name": "John",
    "last_name": "Doe",
    "password1": "password",
    "password2": "password",
}


class SignupFormTest(TestCase):
    def test_pass_normal(self):
        form = UserRegisterForm(data=dummy_user_right)
        self.assertFalse(form.errors)

    def test_fail_username(self):
        form = UserRegisterForm(data=dummy_user_wrong)
        self.assertTrue(form.errors)
        form = UserRegisterForm(data=password_wrong)
        self.assertTrue(form.errors)


class ResetPasswordRequestFormTest(TestCase):
    def test_pass_normal(self):
        form = ResetPasswordRequestForm(data={"username": "Crypt1234"})
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
