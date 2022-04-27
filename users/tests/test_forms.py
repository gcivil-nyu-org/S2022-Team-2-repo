from unittest import TestCase

from users.forms import (
    UserRegisterForm,
    ResetPasswordRequestForm,
    PreferencesExploreForm,
    ResetPasswordForm,
    PreferencesPersonalityForm,
    PreferencesHobbiesForm,
)

dummy_user_right = {
    "username": "test1234",
    "first_name": "John",
    "last_name": "Doe",
    "password1": "Crypt1234",
    "password2": "Crypt1234",
}
dummy_user_wrong = {
    "username": "wrong123username",
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

    def test_fail_password(self):
        form = UserRegisterForm(data=password_wrong)
        self.assertTrue(form.errors)


class ResetPasswordRequestFormTest(TestCase):
    def test_pass_normal(self):
        form = ResetPasswordRequestForm(data={"username": "Crypt1234"})
        self.assertFalse(form.errors)


class ResetPasswordFormTest(TestCase):
    def setUp(self):
        self.correct_password = "Crypt1234"
        self.wrong_password = "test1234"

    def test_pass_normal(self):
        form = ResetPasswordForm(
            data={
                "new_password1": self.correct_password,
                "new_password2": self.correct_password,
            }
        )
        self.assertFalse(form.errors)

    def test_fail(self):
        form = ResetPasswordForm(
            data={
                "new_password1": self.wrong_password,
                "new_password2": self.correct_password,
            }
        )
        self.assertTrue(form.errors)


class PreferencesPersonalityFormTest(TestCase):
    def test_pass(self):
        form = PreferencesPersonalityForm(
            data={
                "personality_type": "Personality_VeryIN",
                "stay_go_type": "Staygo_PI",
            }
        )
        self.assertFalse(form.errors)


class PreferencesHobbiesFormTest(TestCase):
    def test_pass(self):
        form = PreferencesHobbiesForm(
            data={
                "movie_choices": ["Movie_NI"],
                "music_choices": ["MUSIC_NI"],
                "art_choices": ["Art_NI"],
                "dance_choices": ["Dance_NI"],
            }
        )
        self.assertFalse(form.errors)


class PreferencesExploreFormTest(TestCase):
    def test_pass(self):
        form = PreferencesExploreForm(
            data={
                "food_choices": ["Cookeat_NI"],
                "travel_choices": ["Travel_NI"],
                "sports_choices": ["Sports_NI"],
                "nyc_choices": ["Nyc_NI"],
                "pet_choices": ["Pet_NI"],
            }
        )
        self.assertFalse(form.errors)
