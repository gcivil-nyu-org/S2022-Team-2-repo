from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
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


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "image"]


class ResetPasswordRequestForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Net ID"}))


class ResetPasswordForm(forms.Form):
    p_error = None

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

    def clean_password(self):
        error_bool = False
        password1 = self.data["new_password1"]
        try:
            validate_password(password1)
        except ValidationError:
            self.p_error = (
                "Please choose a stronger password.\n"
                "Your password should be at least 8 characters... "
            )
            error_bool = True
            return error_bool, password1
        password2 = self.data["new_password2"]
        if password1 and password2:
            if password1 != password2:
                self.p_error = "Passwords do not match! Please try again."
                error_bool = True
        return error_bool, password2


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


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username"]


class PreferencesPersonalityForm(forms.ModelForm):
    personality_type = forms.ChoiceField(
        choices=PERSONALITY_CHOICES, widget=forms.RadioSelect()
    )
    stay_go_type = forms.ChoiceField(
        choices=STAY_GO_CHOICES, widget=forms.RadioSelect()
    )

    class Meta:
        model = Preference
        fields = [
            "personality_type",
            "stay_go_type",
        ]


class PreferencesMediaForm(forms.ModelForm):
    movie_choices = forms.MultipleChoiceField(
        choices=MOVIES_CHOICES, widget=forms.CheckboxSelectMultiple()
    )
    music_choices = forms.MultipleChoiceField(
        choices=MUSIC_CHOICES, widget=forms.CheckboxSelectMultiple()
    )
    art_choices = forms.MultipleChoiceField(
        choices=ART_CHOICES, widget=forms.CheckboxSelectMultiple()
    )
    dance_choices = forms.MultipleChoiceField(
        choices=DANCE_CHOICES, widget=forms.CheckboxSelectMultiple()
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
        choices=COOKEAT_CHOICES, widget=forms.CheckboxSelectMultiple()
    )
    travel_choices = forms.MultipleChoiceField(
        choices=TRAVEL_CHOICES, widget=forms.CheckboxSelectMultiple()
    )
    sports_choices = forms.MultipleChoiceField(
        choices=SPORTS_CHOICES, widget=forms.CheckboxSelectMultiple()
    )
    nyc_choices = forms.MultipleChoiceField(
        choices=NYC_CHOICES, widget=forms.CheckboxSelectMultiple()
    )
    pet_choices = forms.MultipleChoiceField(
        choices=PET_CHOICES, widget=forms.CheckboxSelectMultiple()
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
