from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        user = UserSerializer
        fields = "__all__"
