from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('',views.home,name="home"),
   path('signup',views.signup,name="signup"),
   path('login',views.login,name="login"),
   path('logout',views.logout,name="logout"),
   path('activate/<uidb64>/<token>/', views.activate, name="activate")
]

