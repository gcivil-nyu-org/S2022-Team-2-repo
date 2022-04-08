from PIL import Image
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from multiselectfield import MultiSelectField

from .preferences import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="default.jpg", upload_to="media", null=True, blank=True
    )
    slug = AutoSlugField(populate_from="user")
    bio = models.CharField(max_length=255, blank=True)
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)  # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img = img.resize(output_size)  # Resize image
            img.save(self.image.path)  # Save it again and override the larger image

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="to_user_friend",
        on_delete=models.CASCADE,
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="from_user_friend",
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)


class Preference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)

    personality_type = MultiSelectField(
        max_length=50,
        choices=PERSONALITY_CHOICES,
        blank=True,
        null=True,
    )
    stay_go_type = MultiSelectField(
        max_length=50,
        choices=STAY_GO_CHOICES,
        blank=True,
        null=True,
    )
    movie_choices = MultiSelectField(
        max_length=50,
        choices=MOVIES_CHOICES,
        blank=True,
        null=True,
    )
    music_choices = MultiSelectField(
        max_length=50,
        choices=MUSIC_CHOICES,
        blank=True,
        null=True,
    )
    food_choices = MultiSelectField(
        max_length=50,
        choices=COOKEAT_CHOICES,
        blank=True,
        null=True,
    )
    travel_choices = MultiSelectField(
        max_length=50,
        choices=TRAVEL_CHOICES,
        blank=True,
        null=True,
    )
    art_choices = MultiSelectField(
        max_length=50,
        choices=ART_CHOICES,
        blank=True,
        null=True,
    )
    dance_choices = MultiSelectField(
        max_length=50,
        choices=DANCE_CHOICES,
        blank=True,
        null=True,
    )
    sports_choices = MultiSelectField(
        max_length=50,
        choices=SPORTS_CHOICES,
        blank=True,
        null=True,
    )
    pet_choices = MultiSelectField(
        max_length=50,
        choices=PET_CHOICES,
        blank=True,
        null=True,
    )
    nyc_choices = MultiSelectField(
        max_length=50,
        choices=NYC_CHOICES,
        blank=True,
        null=True,
    )
