import re

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import FileInput
from django.utils.translation import gettext_lazy as _

from .models import Profile, Preference
from .preferences import *


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Password",
                "data-toggle": "password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Retype Password",
                "data-toggle": "password",
            }
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean(self):
        # Get the user submitted names from the cleaned_data dictionary
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        # NetID validation
        if not re.match(r"^[a-zA-Z]+\d+$", username):
            self.add_error(
                "username",
                "Invalid NetID. Net ID should contain only characters followed by numbers.",
            )

        # Name validation
        if not re.match(r"^[a-zA-Z]+", first_name):
            self.add_error(
                "first_name",
                "Invalid First Name. Cannot contain numbers or special characters.",
            )
        if not re.match(r"^[a-zA-Z]+", last_name):
            self.add_error(
                "last_name",
                "Invalid Last Name. Cannot contain numbers or special characters.",
            )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={"autocomplete": "user-name", "placeholder": "Net ID"}
            ),
            "first_name": forms.TextInput(
                attrs={"autocomplete": "first-name", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"autocomplete": "last-name", "placeholder": "Last Name"}
            ),
        }


class ProfileUpdateForm(forms.ModelForm):  # pragma: no cover
    class Meta:
        model = Profile
        fields = ["bio", "image"]
        widgets = {"image": FileInput()}

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs = {"id": "selectedFile"}


class ResetPasswordRequestForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Net ID"}))


class ResetPasswordForm(forms.Form):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }

    new_password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Password",
                "data-toggle": "password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={"placeholder": "Retype Password", "data-toggle": "password"}
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("new_password2")
        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                self.add_error("new_password2", error)


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("username"),
        strip=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "placeholder": "Net ID",
                "class": "validate",
            }
        ),
    )

    password = forms.CharField(
        label=_("password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Password",
                "data-toggle": "password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )


class PreferencesPersonalityForm(forms.ModelForm):
    personality_type = forms.ChoiceField(
        choices=PERSONALITY_CHOICES,
        widget=forms.RadioSelect(),
        required=True,
        label="Are you more introverted or extroverted?",
    )
    stay_go_type = forms.ChoiceField(
        choices=STAY_GO_CHOICES,
        widget=forms.RadioSelect(),
        required=True,
        label="On a weekend night, do you prefer to stay in or go out?",
    )

    class Meta:
        model = Preference
        fields = [
            "personality_type",
            "stay_go_type",
        ]


class PreferencesHobbiesForm(forms.ModelForm):
    movie_choices = forms.MultipleChoiceField(
        choices=MOVIES_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="What are your favorite movie genres?",
    )
    music_choices = forms.MultipleChoiceField(
        choices=MUSIC_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="What styles of music do you listen to?",
    )
    art_choices = forms.MultipleChoiceField(
        choices=ART_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="What art forms are you interested in?",
    )
    dance_choices = forms.MultipleChoiceField(
        choices=DANCE_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="What dance styles do you like?",
    )

    class Meta:
        model = Preference
        fields = [
            "movie_choices",
            "music_choices",
            "art_choices",
            "dance_choices",
        ]


class PreferencesExploreForm(forms.ModelForm):
    food_choices = forms.MultipleChoiceField(
        choices=COOKEAT_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="What are your favorite cuisines?",
    )
    travel_choices = forms.MultipleChoiceField(
        choices=TRAVEL_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="What's your ideal vacation spot?",
    )
    sports_choices = forms.MultipleChoiceField(
        choices=SPORTS_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="What sports do you like to play or watch?",
    )
    pet_choices = forms.MultipleChoiceField(
        choices=PET_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="What kind of pets do you have?",
    )
    nyc_choices = forms.MultipleChoiceField(
        choices=NYC_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="What do you like to do around NYC?",
    )

    class Meta:
        model = Preference
        fields = [
            "food_choices",
            "travel_choices",
            "sports_choices",
            "pet_choices",
            "nyc_choices",
        ]
