from django.contrib.auth import views as auth_views
from django.urls import path

from users import views as user_views
from users.forms import LoginForm

urlpatterns = [
    path("", user_views.home, name="home"),
    path("signup", user_views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html", authentication_form=LoginForm),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("activate/<uidb64>/<token>/", user_views.activate, name="activate"),
    path("activate", user_views.signup, name="activate2"),
    path(
        "password_reset_request",
        user_views.password_reset_request,
        name="password_reset_request",
    ),
    path(
        "reset_password/<uidb64>/<token>/",
        user_views.password_reset,
        name="reset_password",
    ),
]
