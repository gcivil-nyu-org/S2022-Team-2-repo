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
    preferences,
    update_profile,
    search,
    my_friends,
    friend_request_query,
    notifications,
    accept_request_query,
    decline_request_query,
    FriendsListView,
    SelfView,
    self_info,
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

    def test_dashboard_preference_url_resolves(self):
        url = reverse("preferences")
        self.assertEquals(resolve(url).func, preferences)

    def test_update_profile_url_resolves(self):
        url = reverse("profile")
        self.assertEquals(resolve(url).func, update_profile)

    def test_search_profile_url_resolves(self):
        url = reverse("search")
        self.assertEquals(resolve(url).func, search)

    def test_my_friends_url_resolves(self):
        url = reverse("my_friends")
        self.assertEquals(resolve(url).func, my_friends)

    def test_notification_count_url_resolves(self):
        url = reverse("notification_count")
        self.assertEquals(resolve(url).func, notifications)

    def test_friend_request_url_resolves(self):
        url = reverse("friend_request")
        self.assertEquals(resolve(url).func, friend_request_query)

    def test_accept_request_url_resolves(self):
        url = reverse("accept_request")
        self.assertEquals(resolve(url).func, accept_request_query)

    def test_decline_request_url_resolves(self):
        url = reverse("decline_request")
        self.assertEquals(resolve(url).func, decline_request_query)

    def test_friends_list_url_resolves(self):
        url = reverse("friends_list")
        self.assertEquals(resolve(url).func.view_class, FriendsListView)

    def test_user_info_url_resolves(self):
        url = reverse("user_info", args=["test-slug"])
        self.assertEquals(resolve(url).func.view_class, SelfView)

    def test_self_info_url_resolves(self):
        url = reverse("self_info")
        self.assertEquals(resolve(url).func, self_info)
