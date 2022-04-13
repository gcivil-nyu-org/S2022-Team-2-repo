from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from users.models import Profile, Preference

dummy_user_right = {
    "username": "test1234",
    "email": "test1234@nyu.edu",
    "first_name": "John",
    "last_name": "Doe",
    "password": "Crypt1234",
}


class LoginViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_get_page(self):
        response = self.client.get(reverse("login"))
        self.assertTrue(response.status_code, 200)

    def test_call_view_pass(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": dummy_user_right["username"],
                "password": dummy_user_right["password"],
            },
            follow=True,
        )
        self.assertEquals(response.status_code, 200)


class LogoutViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("logout"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("logout"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("logout"))
        self.assertTrue(response.status_code, 200)

    def test_redirect_successful_logout(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("logout"), follow=True)
        self.assertRedirects(response, "/")


class ProfileSetupTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )
        cls.profile = Profile(user=user)

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("profile_setup"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("profile_setup"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile_setup"))
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("profile_setup"), data={"bio": "Test"})
        self.assertTrue(response.status_code, 200)


class UpdateProfileTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )
        cls.profile = Profile(user=user)

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("profile"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("profile"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile"))
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("profile"), data={"bio": "Test"})
        self.assertTrue(response.status_code, 200)


class PersonalityPreferenceTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )
        cls.preferences = Preference(user=user)

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("preferences_personality"), follow=True)
        self.assertRedirects(
            response, "/login/?next=" + reverse("preferences_personality")
        )

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("preferences_personality"))
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("preferences_personality"),
            data={"personality_type": "VeryIN", "stay_go_type": "PI"},
            follow=True,
        )
        self.assertRedirects(response, reverse("preferences_hobbies"))
        self.assertTrue(response.status_code, 200)


class HobbiesPreferenceTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )
        cls.preferences = Preference(user=user)

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("preferences_hobbies"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("preferences_hobbies"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("preferences_hobbies"))
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("preferences_hobbies"),
            data={
                "movie_choices": ["NI"],
                "music_choices": ["NI"],
                "art_choices": ["NI"],
                "dance_choices": ["NI"],
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("preferences_explore"))
        self.assertTrue(response.status_code, 200)


class ExplorePreferenceTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )
        cls.preferences = Preference(user=user)

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("preferences_explore"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("preferences_explore"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("preferences_explore"))
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("profile"),
            data={
                "food_choices": ["NI"],
                "travel_choices": ["NI"],
                "sports_choices": ["NI"],
                "nyc_choices": ["NI"],
                "pet_choices": ["NI"],
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(response.status_code, 200)


class DashboardViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("dashboard"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertTrue(response.status_code, 200)

    def test_redirect_successful_login_redirect(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": dummy_user_right["username"],
                "password": dummy_user_right["password"],
            },
            follow=True,
        )
        self.assertEquals(response.status_code, 200)


class SearchViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("search"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("search"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("search"))
        self.assertTrue(response.status_code, 200)


class FriendRequestTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("friend_request"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("friend_request"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("friend_request"))
        self.assertTrue(response.status_code, 200)


class AcceptRequestTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user1 = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("accept_request"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("accept_request"))

    def test_call_get_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("accept_request"))
        self.assertTrue(response.status_code, 200)


class DeclineRequestTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user1 = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("decline_request"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("decline_request"))

    def test_call_get_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("decline_request"))
        self.assertTrue(response.status_code, 200)


class FriendsListTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user1 = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("my_friends"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("my_friends"))

    def test_call_get_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("my_friends"))
        self.assertTrue(response.status_code, 200)


class NotificationsTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user1 = User.objects.create_user(
            username=dummy_user_right["username"], password=dummy_user_right["username"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("notification_count"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("notification_count"))

    def test_call_get_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("notification_count"))
        self.assertTrue(response.status_code, 200)
