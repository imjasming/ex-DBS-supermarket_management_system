from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext, gettext_lazy as _

from .models import Customer, Branch, Staff

User = get_user_model()


class AdminLoginForm(forms.Form):
    ID = forms.CharField(label='ID', max_length=20,
                         widget=forms.TextInput(
                             attrs={'class': 'form-control', 'placeholder': 'your staff id'}))
    password = forms.CharField(label='Password', min_length=6, max_length=18,
                               widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))


class LoginForm(forms.Form):
    id = forms.CharField(label='ID', max_length=20,
                         widget=forms.TextInput(
                             attrs={'class': 'form-control', 'placeholder': 'Your id'}))
    password = forms.CharField(label='Password', min_length=6, max_length=18,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ChangeEmailForm(forms.Form):
    nickname = forms.CharField(label='Nickname', max_length=20,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Nickname'}))

    def clean_email(self):
        nickname = self.cleaned_data['Nickname']
        email_filter = Customer.objects.filter(CName=nickname)
        if len(email_filter) > 0:
            raise forms.ValidationError(
                _('nickname already taken.'), code='invalid nickname'
            )


class MyPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("password"),
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(),
    )
    error_messages = {
        **PasswordChangeForm.error_messages,
        'password_incorrect': _("invalid password."),
    }

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

