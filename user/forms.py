import unicodedata
from django import forms
from django.contrib.auth import (password_validation, )
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


class ResetPasswordRequestForm(forms.Form):
    netid = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'NetID'}))


class ResetPasswordForm(forms.Form):

    p_error = None

    new_password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Retype Password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_password(self):
        error_bool = False
        password1 = self.data['new_password1']
        password2 = self.data['new_password2']
        if password1 and password2:
            if password1 != password2:
                self.p_error = 'Passwords do not match! Please try again.'
                error_bool = True
        return error_bool, password2


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserDetails

        fields = ['netid', 'password']

        labels = {
            'netid': '',
            'password': '',
        }

        widgets = {
            'netid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Net ID'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserDetails
        fields = ('netid',)
        field_classes = {'netid': NetIdField}
