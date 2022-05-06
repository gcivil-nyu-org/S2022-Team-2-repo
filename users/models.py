from PIL import Image
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.urls import reverse
from multiselectfield import MultiSelectField

from .preferences import *


def report_email(user):
    to_email = user.username + "@nyu.edu"
    mail_subject = "From NYUnite Admin Team: Your account has been removed"
    message = render_to_string(
        "users/report_email.html",
        {"user": user},
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="media/default.png", upload_to="media", null=True, blank=True
    )
    slug = AutoSlugField(populate_from="user")
    bio = models.CharField(max_length=255, blank=True)
    friends = models.ManyToManyField("Profile", blank=True, related_name="friend_list")
    seen_users = models.ManyToManyField("Profile", blank=True, related_name="seen_list")
    favorites = models.ManyToManyField(
        "Profile", blank=True, related_name="favorite_list"
    )
    blocked = models.ManyToManyField("Profile", blank=True, related_name="blocked_list")
    blockers = models.ManyToManyField(
        "Profile", blank=True, related_name="blockers_list"
    )

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = None
        try:
            img = Image.open(self.image.name)
        except Exception as e:
            print(e)
            img = Image.open("media/default.png")

        if img.width > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.name)
            self.image = img

    def get_absolute_url(self):
        return reverse("user_info", kwargs={"slug": self.slug})


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


class Blacklist(models.Model):
    blacklisted = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="blacklisted_user"
    )

    def __str__(self):
        return f"{self.blacklisted}"


class Report(models.Model):
    reporter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reporter_user", default=None
    )
    reported = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reported_user", default=None
    )
    reason = models.CharField(max_length=1000, blank=True)
    status = models.CharField(
        max_length=10,
        choices=(
            ("received", "received"),
            ("ignored", "ignored"),
            ("approved", "approved"),
        ),
        default="received",
    )

    def __str__(self):
        return f"Report of {self.reported} by {self.reporter}"

    def save(self, *args, **kwargs):
        super(Report, self).save(*args, **kwargs)

        if self.status == "approved":
            blacklist_record = Blacklist(blacklisted=self.reported)
            blacklist_record.save()
            user = User.objects.get(pk=self.reported.id)
            user.is_active = False
            user.save()
            reports = Report.objects.all().filter(reported=user)
            reports.update(status="approved")
            report_email(user)


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
        max_length=200,
        choices=PERSONALITY_CHOICES,
        blank=True,
        null=True,
    )
    stay_go_type = MultiSelectField(
        max_length=200,
        choices=STAY_GO_CHOICES,
        blank=True,
        null=True,
    )
    movie_choices = MultiSelectField(
        max_length=200,
        choices=MOVIES_CHOICES,
        blank=True,
        null=True,
    )
    music_choices = MultiSelectField(
        max_length=200,
        choices=MUSIC_CHOICES,
        blank=True,
        null=True,
    )
    food_choices = MultiSelectField(
        max_length=200,
        choices=COOKEAT_CHOICES,
        blank=True,
        null=True,
    )
    travel_choices = MultiSelectField(
        max_length=200,
        choices=TRAVEL_CHOICES,
        blank=True,
        null=True,
    )
    art_choices = MultiSelectField(
        max_length=200,
        choices=ART_CHOICES,
        blank=True,
        null=True,
    )
    dance_choices = MultiSelectField(
        max_length=200,
        choices=DANCE_CHOICES,
        blank=True,
        null=True,
    )
    sports_choices = MultiSelectField(
        max_length=200,
        choices=SPORTS_CHOICES,
        blank=True,
        null=True,
    )
    pet_choices = MultiSelectField(
        max_length=200,
        choices=PET_CHOICES,
        blank=True,
        null=True,
    )
    nyc_choices = MultiSelectField(
        max_length=200,
        choices=NYC_CHOICES,
        blank=True,
        null=True,
    )
