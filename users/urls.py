from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

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
    path("user/friends/accept", user_views.accept_request_query, name="accept_request"),
    path(
        "user/friends/decline", user_views.decline_request_query, name="decline_request"
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
