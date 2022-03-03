from django import forms
from user.models import UserDetails


class SignupForm(forms.ModelForm):
    password_retype = forms.CharField(label='', max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Retype Password'}))

    class Meta:
        model = UserDetails
        fields = ('netID', 'first_name', 'middle_name', 'last_name', 'password')

        labels = {
            'netID': '',
            'first_name': '',
            'middle_name': '',
            'last_name': '',
            'password': '',
        }

        widgets = {
            'netID': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Net ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }


class ResetPasswordForm(forms.ModelForm):
    class Meta:
        model = UserDetails

        fields = ['netID', ]

        labels = {'netID': '', }

        widgets = {'netID': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Net ID'}), }


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserDetails

        fields = ['netID', 'password']

        labels = {
            'netID': '',
            'password': '',
        }

        widgets = {
            'netID': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Net ID'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }

