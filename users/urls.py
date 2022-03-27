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
    path(
        "preferences/page1",
        user_views.preferences_personality,
        name="preferences_personality",
    ),
    path(
        "preferences/page2", user_views.preferences_hobbies, name="preferences_hobbies"
    ),
    path("dashboard/", user_views.dashboard, name="dashboard"),
    path("dashboard/preferences/", user_views.preferences, name="preferences"),
    path("updateprofile/", user_views.profile, name="profile"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
