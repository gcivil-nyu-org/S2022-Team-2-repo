from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from users.models import Profile, Preference

dummy_user = {
    "username": "test1234",
    "email": "test1234@nyu.edu",
    "first_name": "John",
    "last_name": "Doe",
    "password": "Crypt1234",
}


class HomeViewTest(TestCase):
    def test_call_get_page(self):
        response = self.client.get(reverse("home"))
        self.assertTrue(response.status_code, 200)


class LoginViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_get_page(self):
        response = self.client.get(reverse("login"))
        self.assertTrue(response.status_code, 200)

    def test_call_auto_redirect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("login"), follow=True)
        self.assertTrue(response.status_code, 200)

    def test_call_view_pass(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": dummy_user["username"],
                "password": dummy_user["password"],
            },
            follow=True,
        )
        self.assertEquals(response.status_code, 200)

    def test_call_view_redirect_setup(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": dummy_user["username"] + "1",
                "password": dummy_user["password"],
            },
            follow=True,
        )
        self.assertEquals(response.status_code, 200)


class LogoutViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
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
            username=dummy_user["username"], password=dummy_user["password"]
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
            username=dummy_user["username"], password=dummy_user["password"]
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
            username=dummy_user["username"], password=dummy_user["password"]
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
            data={
                "personality_type": "Personality_VeryIN",
                "stay_go_type": "Staygo_PI",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("preferences_hobbies"))
        self.assertTrue(response.status_code, 200)


class HobbiesPreferenceTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
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
                "movie_choices": ["Movie_NI"],
                "music_choices": ["MUSIC_NI"],
                "art_choices": ["Art_NI"],
                "dance_choices": ["Dance_NI"],
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
            username=dummy_user["username"], password=dummy_user["password"]
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
            reverse("preferences_explore"),
            data={
                "food_choices": ["Cookeat_NI"],
                "travel_choices": ["Travel_NI"],
                "sports_choices": ["Sports_NI"],
                "nyc_choices": ["Nyc_NI"],
                "pet_choices": ["Pet_NI"],
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(response.status_code, 200)


class FriendsListTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("friends_list"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("friends_list"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("friends_list"))
        self.assertTrue(response.status_code, 200)


class SelfViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(
            reverse("user_info", args=[self.user.username]), follow=True
        )
        self.assertRedirects(
            response, "/login/?next=" + reverse("user_info", args=[self.user.username])
        )

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("user_info", args=[self.user.username]))
        self.assertTrue(response.status_code, 200)


class SelfInfoTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("self_info"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("self_info"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("self_info"))
        self.assertTrue(response.status_code, 200)


class FavouriteTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.profile = Profile(user)
        cls.user2 = user2 = User.objects.create_user(
            username=dummy_user["username"] + "1", password=dummy_user["password"]
        )
        cls.profile2 = Profile(user2)

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("favorite"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("favorite"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("favorite"), data={"favorite": str(self.user2.pk)}
        )
        self.assertTrue(response.status_code, 200)


class DashboardViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
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
                "username": dummy_user["username"],
                "password": dummy_user["password"],
            },
            follow=True,
        )
        self.assertEquals(response.status_code, 200)


class PreferenceViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("preferences"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("preferences"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("preferences"))
        self.assertTrue(response.status_code, 200)


class SearchViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
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
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.user2 = User.objects.create_user(
            username=dummy_user["username"] + "1",
            password=dummy_user["password"],
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("friend_request"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("friend_request"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("friend_request"))
        self.assertTrue(response.status_code, 200)

    def test_send_request(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("friend_request"),
            {
                "friendRequest": self.user2.id,
            },
        )
        self.assertTrue(response.status_code, 200)


class AcceptRequestTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.user2 = User.objects.create_user(
            username=dummy_user["username"] + "1",
            password=dummy_user["password"],
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("accept_request"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("accept_request"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("accept_request"))
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("friend_request"),
            {
                "friendRequest": self.user2.id,
            },
        )
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse("accept_request"), {"acceptRequest": self.user.id}
        )
        self.assertTrue(response.status_code, 200)


class DeclineRequestTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.user2 = User.objects.create_user(
            username=dummy_user["username"] + "1",
            password=dummy_user["password"],
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("decline_request"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("decline_request"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("decline_request"))
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("friend_request"),
            {
                "friendRequest": self.user2.id,
            },
        )
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse("decline_request"), {"declineRequest": self.user.id}
        )
        self.assertTrue(response.status_code, 200)


class MyFriendsTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("my_friends"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("my_friends"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("my_friends"))
        self.assertTrue(response.status_code, 200)


class NotificationsTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("notification_count"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("notification_count"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("notification_count"))
        self.assertTrue(response.status_code, 200)


class ChatNotificationsTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("chat_unread_count"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("chat_unread_count"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("chat_unread_count"))
        self.assertTrue(response.status_code, 200)


class DeclineSuggestionTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.user2 = User.objects.create_user(
            username=dummy_user["username"] + "1",
            password=dummy_user["password"],
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("reject-suggestion"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("reject-suggestion"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reject-suggestion"))
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("reject-suggestion"), {"friendID": self.user2.id}
        )
        self.assertTrue(response.status_code, 200)


class AcceptSuggestionTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.user2 = User.objects.create_user(
            username=dummy_user["username"] + "1",
            password=dummy_user["password"],
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("approve-suggestion"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("approve-suggestion"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("approve-suggestion"))
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("approve-suggestion"), {"friendID": self.user2.id}
        )
        self.assertTrue(response.status_code, 200)


class FriendMatcherTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.preferences = Preference(user=user)
        cls.user2 = user2 = User.objects.create_user(
            username=dummy_user["username"] + "1", password=dummy_user["password"]
        )
        cls.preferences = Preference(user=user2)

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("friend-finder"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("friend-finder"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("friend-finder"))
        self.assertTrue(response.status_code, 200)


class ActivitySearchTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("activity_search"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("activity_search"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("activity_search"))
        self.assertTrue(response.status_code, 200)


class ActivityTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("activity"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("activity"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("activity"))
        self.assertTrue(response.status_code, 200)


class ReportTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.user2 = User.objects.create_user(
            username=dummy_user["username"] + "1",
            password=dummy_user["password"],
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("report"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("report"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("report"))
        self.assertTrue(response.status_code, 500)

    def test_call_success(self):
        self.client.force_login(self.user)
        data = {"user": self.user, "report": self.user2.id, "text": "dummy_text"}
        response = self.client.post(
            reverse("report"),
            data,
        )
        self.assertTrue(response.status_code, 200)


class BlockTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.user2 = User.objects.create_user(
            username=dummy_user["username"] + "1",
            password=dummy_user["password"],
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("block"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("block"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("block"))
        self.assertTrue(response.status_code, 500)

    def test_call_success(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("friend_request"),
            {
                "friendRequest": self.user2.id,
            },
        )
        self.client.post(reverse("favorite"), data={"favorite": str(self.user2.pk)})
        self.client.logout()
        self.client.force_login(self.user2)
        self.client.post(reverse("accept_request"), {"acceptRequest": self.user.id})
        self.client.post(reverse("favorite"), data={"favorite": str(self.user.pk)})
        data = {"user": self.user2, "blocked": self.user.id}
        response = self.client.post(
            reverse("block"),
            data,
        )
        self.assertTrue(response.status_code, 200)


class RemoveFriendTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.user2 = User.objects.create_user(
            username=dummy_user["username"] + "1",
            password=dummy_user["password"],
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("remove"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("remove"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("remove"), {"user": self.user})
        self.assertTrue(response.status_code, 500)

    def test_call_success(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("friend_request"),
            {
                "friendRequest": self.user2.id,
            },
        )
        self.client.post(reverse("favorite"), data={"favorite": str(self.user2.pk)})
        self.client.logout()
        self.client.force_login(self.user2)
        self.client.post(reverse("accept_request"), {"acceptRequest": self.user.id})
        self.client.post(reverse("favorite"), data={"favorite": str(self.user.pk)})
        response = self.client.post(
            reverse("remove"),
            {
                "remove": self.user.id,
            },
        )
        self.assertTrue(response.status_code, 200)


class ReactivateTest(TestCase):
    def test_call_get_page(self):
        response = self.client.get(
            reverse("reactivate"), {"username": dummy_user["username"]}
        )
        self.assertTrue(response.status_code, 200)

    def test_call_no_username(self):
        response = self.client.get(reverse("reactivate"))
        self.assertTrue(response.status_code, 200)


class DeleteProfileTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("delete_profile"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("delete_profile"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_profile"))
        self.assertTrue(response.status_code, 200)


class BlockedListTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.user2 = User.objects.create_user(
            username=dummy_user["username"] + "1",
            password=dummy_user["password"],
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("blocked_list"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("blocked_list"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("blocked_list"))
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        data = {"user": self.user, "blocked": self.user2.id}
        self.client.post(
            reverse("block"),
            data,
        )
        response = self.client.get(reverse("blocked_list"))
        self.assertTrue(response.status_code, 200)


class UnblockTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username=dummy_user["username"], password=dummy_user["password"]
        )
        cls.user2 = User.objects.create_user(
            username=dummy_user["username"] + "1",
            password=dummy_user["password"],
        )

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse("unblock"), follow=True)
        self.assertRedirects(response, "/login/?next=" + reverse("unblock"))

    def test_call_get_page(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("unblock"), {"user": self.user, "unblock": self.user2.id}
        )
        self.assertTrue(response.status_code, 200)

    def test_call_success(self):
        self.client.force_login(self.user)
        data = {"user": self.user, "blocked": self.user2.id}
        self.client.post(
            reverse("block"),
            data,
        )
        data = {"user": self.user, "unblock": self.user2.id}
        response = self.client.post(reverse("unblock"), data)
        self.assertTrue(response.status_code, 200)
