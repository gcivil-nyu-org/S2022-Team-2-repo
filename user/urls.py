from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('',views.home,name="home"),
   path('signup',views.signup,name="signup"),
   path('login',views.login_form,name="login"),
   path('logout',views.logout,name="logout"),
   path('activate/<uidb64>/<token>/', views.activate, name="activate"),
   path('activate', views.signup, name="activate2"),
   path('password_reset_request', views.password_reset_request, name="password_reset_request"),
   path('dashboard', views.dashboard, name="dashboard"),
   path('reset_password/<uidb64>/<token>/', views.password_reset, name="reset_password"),
]

