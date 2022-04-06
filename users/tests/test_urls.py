from django.urls import reverse, resolve
from django.test import SimpleTestCase

from users.views import (
    home,
    signup,
    login_form,
    logout_request,
    password_reset_request,
    profile_setup,
    preferences_personality,
    preferences_hobbies,
    preferences_explore,
    dashboard,
)


class TestUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse("home")
        self.assertEquals(resolve(url).func, home)

    def test_signup_url_resolves(self):
        url = reverse("signup")
        self.assertEquals(resolve(url).func, signup)

    def test_login_url_resolves(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func, login_form)

    def test_logout_url_resolves(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func, logout_request)

    def test_password_reset_request_url_resolves(self):
        url = reverse("password_reset_request")
        self.assertEquals(resolve(url).func, password_reset_request)

    def test_profile_setup_url_resolves(self):
        url = reverse("profile_setup")
        self.assertEquals(resolve(url).func, profile_setup)

    def test_preferences_personality_url_resolves(self):
        url = reverse("preferences_personality")
        self.assertEquals(resolve(url).func, preferences_personality)

    def test_preferences_hobbies_url_resolves(self):
        url = reverse("preferences_hobbies")
        self.assertEquals(resolve(url).func, preferences_hobbies)

    def test_preferences_explore_url_resolves(self):
        url = reverse("preferences_explore")
        self.assertEquals(resolve(url).func, preferences_explore)

    def test_dashboard_url_resolves(self):
        url = reverse("dashboard")
        self.assertEquals(resolve(url).func, dashboard)
