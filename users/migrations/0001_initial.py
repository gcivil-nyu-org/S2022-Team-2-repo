# Generated by Django 4.0.2 on 2022-04-14 20:43

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, default="default.jpg", null=True, upload_to="media"
                    ),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(editable=False, populate_from="user"),
                ),
                ("bio", models.CharField(blank=True, max_length=255)),
                (
                    "friends",
                    models.ManyToManyField(
                        blank=True, related_name="friend_list", to="users.Profile"
                    ),
                ),
                (
                    "seen_users",
                    models.ManyToManyField(
                        blank=True, related_name="seen_list", to="users.Profile"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Preference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "personality_type",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Personality_VeryEX", "Very Extroverted"),
                            ("Personality_SomewhatEX", "Somewhat Extroverted"),
                            ("Personality_Neutral", "Neutral"),
                            ("Personality_SomewhatIN", "Somewhat Introverted"),
                            ("Personality_VeryIN", "Very Introverted"),
                        ],
                        max_length=103,
                        null=True,
                    ),
                ),
                (
                    "stay_go_type",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Staygo_PI", "Prefer to Stay In"),
                            ("Staygo_PO", "Prefer to Go Out"),
                        ],
                        max_length=19,
                        null=True,
                    ),
                ),
                (
                    "movie_choices",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Movie_AC", "Action"),
                            ("Movie_CO", "Comedy"),
                            ("Movie_DR", "Drama"),
                            ("Movie_FN", "Fantasy"),
                            ("Movie_HR", "Horror"),
                            ("Movie_MY", "Mystery"),
                            ("Movie_RO", "Romance"),
                            ("Movie_TH", "Thriller"),
                            ("Movie_NI", "Not interested in Movies"),
                        ],
                        max_length=80,
                        null=True,
                    ),
                ),
                (
                    "music_choices",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Music_RO", "Rock"),
                            ("MUSIC_PO", "Pop"),
                            ("MUSIC_HIHO", "Hiphop"),
                            ("MUSIC_RP", "Rap"),
                            ("MUSIC_CL", "Classical"),
                            ("MUSIC_IN", "Indian"),
                            ("MUSIC_NI", "Not interested in Music"),
                        ],
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "food_choices",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Cookeat_CA", "Caribbean"),
                            ("Cookeat_MX", "Mexican"),
                            ("Cookeat_MED", "Mediterranean"),
                            ("Cookeat_KO", "Korean"),
                            ("Cookeat_VT", "Vietnamese"),
                            ("Cookeat_IN", "Indian"),
                            ("Cookeat_CH", "Chinese"),
                            ("Cookeat_FN", "French"),
                            ("Cookeat_IT", "Italian"),
                            ("Cookeat_TH", "Thai"),
                            ("Cookeat_LB", "Lebanese"),
                            ("Cookeat_AM", "American"),
                            ("Cookeat_NI", "Not interested in Cooking/Cuisines"),
                        ],
                        max_length=143,
                        null=True,
                    ),
                ),
                (
                    "travel_choices",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Travel_MO", "Mountains"),
                            ("Travel_BE", "Beaches"),
                            ("Travel_DE", "Desserts"),
                            ("Travel_IP", "Ice Places"),
                            ("Travel_CT", "City"),
                            ("Travel_VI", "Village"),
                            ("Travel_NI", "Not interested in Traveling"),
                        ],
                        max_length=69,
                        null=True,
                    ),
                ),
                (
                    "art_choices",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Art_DR", "Drawing"),
                            ("Art_SK", "Sketching"),
                            ("Art_PA", "Painting"),
                            ("Art_PM", "Printmaking"),
                            ("Art_JM", "Jewelery Making"),
                            ("Art_PH", "Photography"),
                            ("Art_SL", "Sculpture"),
                            ("Art_CA", "Calligraphy"),
                            ("Art_NI", "Not interested in Art"),
                        ],
                        max_length=62,
                        null=True,
                    ),
                ),
                (
                    "dance_choices",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Dance_HH", "HipHop"),
                            ("Dance_CP", "Contemporary"),
                            ("Dance_JZ", "Jazz"),
                            ("Dance_BL", "Ballet"),
                            ("Dance_BA", "Ballroom"),
                            ("Dance_TD", "Tap Dance"),
                            ("Dance_ID", "Irish Dance"),
                            ("Dance_BO", "Bollywood"),
                            ("Dance_SW", "Swing"),
                            ("Dance_NI", "Not interested in Dance"),
                        ],
                        max_length=89,
                        null=True,
                    ),
                ),
                (
                    "sports_choices",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Sports_FB", "Football"),
                            ("Sports_BK", "Basketball"),
                            ("Sports_CR", "Cricket"),
                            ("Sports_HC", "Hockey"),
                            ("Sports_BB", "Baseball"),
                            ("Sports_SFB", "Softball"),
                            ("Sports_GM", "Gymnastics"),
                            ("Sports_SKB", "Skateboard"),
                            ("Sports_RW", "Rowing"),
                            ("Sports_RB", "Rugby"),
                            ("Sports_LC", "Lacrosse"),
                            ("Sports_SW", "Swimming"),
                            ("Sports_SC", "Soccer"),
                            ("Sports_RU", "Running"),
                            ("Sports_VB", "Volleyball"),
                            ("Sports_SWB", "Snowboarding"),
                            ("Sports_SK", "Skiing"),
                            ("Sports_MA", "Martial arts"),
                            ("Sports_GO", "Golf"),
                            ("Sports_BC", "Bicycling"),
                            ("Sports_NI", "Not interested in Sports"),
                        ],
                        max_length=212,
                        null=True,
                    ),
                ),
                (
                    "pet_choices",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Pet_DG", "Dogs"),
                            ("Pet_CT", "Cats"),
                            ("Pet_BI", "Birds"),
                            ("Pet_FI", "Fish"),
                            ("Pet_HR", "Horses"),
                            ("Pet_RT", "Reptiles"),
                            ("Pet_NI", "Not interested in Pets"),
                        ],
                        max_length=48,
                        null=True,
                    ),
                ),
                (
                    "nyc_choices",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Nyc_MU", "Visiting Museum"),
                            ("Nyc_CN", "Concerts"),
                            ("Nyc_BA", "Bars"),
                            ("Nyc_PK", "Park"),
                            ("Nyc_CL", "Club"),
                            ("Nyc_TH", "Theater"),
                            ("Nyc_SW", "Street walk"),
                            ("Nyc_NI", "Not interested in Exploring NYC"),
                        ],
                        max_length=55,
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FriendRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "from_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="from_user_friend",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "to_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="to_user_friend",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
