import unicodedata
from django import forms
from django.contrib.auth import (
    password_validation, )
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import UserDetails


class NetIdField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'netid',
            'placeholder': 'Net ID'
        }


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Retype Password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = UserDetails
        fields = ('netid', 'first_name', 'middle_name', 'last_name')
        field_classes = {'netid': NetIdField}
        widgets = {
            'first_name': forms.TextInput(attrs={'autocomplete': 'email', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'autocomplete': 'email', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'autocomplete': 'email', 'placeholder': 'Last Name'}),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserDetails
        fields = ('netid',)
        field_classes = {'netid': NetIdField}
