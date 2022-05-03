from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include
from django.views.generic import TemplateView

import users.views
from users import views as user_views

urlpatterns = [
    path("", user_views.home, name="home"),
    path("signup/", user_views.signup, name="signup"),
    path("login/", user_views.login_form, name="login"),
    path(
        "logout/",
        user_views.logout_request,
        name="logout",
    ),
    path("activate/<uidb64>/<token>/", user_views.activate, name="activate"),
    path("activate", user_views.signup, name="activate2"),
    path(
        "login/password_reset_request/",
        user_views.password_reset_request,
        name="password_reset_request",
    ),
    path(
        "reset_password/<uidb64>/<token>/",
        user_views.password_reset,
        name="reset_password",
    ),
    path("profile/setup", user_views.profile_setup, name="profile_setup"),
    path("profile/delete", user_views.delete_profile, name="delete_profile"),
    path(
        "preferences/page1",
        user_views.preferences_personality,
        name="preferences_personality",
    ),
    path(
        "preferences/page2", user_views.preferences_hobbies, name="preferences_hobbies"
    ),
    path(
        "preferences/page3", user_views.preferences_explore, name="preferences_explore"
    ),
    path("dashboard/", user_views.dashboard, name="dashboard"),
    path("dashboard/preferences/", user_views.preferences, name="preferences"),
    path(
        "dashboard/preferences/updateprofile/",
        user_views.update_profile,
        name="profile",
    ),
    path("dashboard/search", user_views.search, name="search"),
    path("dashboard/my_friends", user_views.my_friends, name="my_friends"),
    path(
        "user/friends/request", user_views.friend_request_query, name="friend_request"
    ),
    path(
        "user/notification/count", user_views.notifications, name="notification_count"
    ),
    path(
        "user/notification/chat",
        user_views.chat_notifications,
        name="chat_unread_count",
    ),
    path("user/friends/accept", user_views.accept_request_query, name="accept_request"),
    path(
        "user/friends/decline", user_views.decline_request_query, name="decline_request"
    ),
    re_path(
        r"", include("django_private_chat2.urls", namespace="django_private_chat2")
    ),  # pragma: no cover
    path("user/friends", user_views.FriendsListView.as_view(), name="friends_list"),
    path("user/<slug>/", user_views.SelfView.as_view(), name="user_info"),
    path("user/self", user_views.self_info, name="self_info"),
    path(
        "dashboard/chat",
        login_required(TemplateView.as_view(template_name="users/chat.html")),
        name="chat",
    ),  # pragma: no cover
    path("dashboard/friend_finder", user_views.friend_finder, name="friend-finder"),
    path(
        "activity_search",
        users.views.activity_search,
        name="activity_search",
    ),
    path("suggestion/reject", user_views.reject_suggestion, name="reject-suggestion"),
    path(
        "suggestion/approve", user_views.approve_suggestion, name="approve-suggestion"
    ),
    path("dashboard/activity", user_views.activity, name="activity"),
    path("dashboard/favorite", user_views.favorite, name="favorite"),
    path("user/friend/block", user_views.block, name="block"),
    path("user/unblock", user_views.unblock, name="unblock"),
    path("user/blocked", user_views.blocked_list, name="blocked_list"),
    path("user/friend/remove", user_views.remove_friend, name="remove"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
