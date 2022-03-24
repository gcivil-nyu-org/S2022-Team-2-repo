from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from .preferences import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_pics")
    slug = AutoSlugField(populate_from="user")
    bio = models.CharField(max_length=255, blank=True)

    # friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="to_user", on_delete=models.CASCADE
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="from_user", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)


class Preference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)

    bio = models.CharField(max_length=255, blank=True)

    personality_type = models.CharField(
        max_length=50,
        choices=PERSONALITY_CHOICES,
    )
    stay_go_type = models.CharField(
        max_length=50,
        choices=STAY_GO_CHOICES,
    )
    movie_choices = models.CharField(
        max_length=50,
    )
    music_choices = models.CharField(
        max_length=50,
        choices=MUSIC_CHOICES,
    )
    food_choices = models.CharField(
        max_length=50,
        choices=COOKEAT_CHOICES,
    )
    travel_choices = models.CharField(
        max_length=50,
        choices=TRAVEL_CHOICES,
    )
    art_choices = models.CharField(
        max_length=50,
        choices=ART_CHOICES,
    )
    dance_choices = models.CharField(
        max_length=50,
        choices=DANCE_CHOICES,
    )
    sports_choices = models.CharField(
        max_length=50,
        choices=SPORTS_CHOICES,
    )
    pet_choices = models.CharField(
        max_length=50,
        choices=PET_CHOICES,
    )
    nyc_choices = models.CharField(
        max_length=50,
        choices=NYC_CHOICES,
    )
