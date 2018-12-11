from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext, gettext_lazy as _

from .models import Customer, Branch, Staff


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



#登录表单
class UserForm(forms.Form):
    id = forms.CharField(required=True,max_length=20)
    password = forms.CharField(min_length=11)
    def clean_id(self):
        id = self.cleaned_data.get('id')
        if id:
            filter_result = User.objects.filter(id=email)
            if not filter_result:
                raise forms.ValidationError("id not found.")
        return id


class RegistrationForm(forms.Form):
    username = forms.CharField(required=True,max_length=20)
    tel = forms.CharField(required=True,max_length=11)
    password = forms.CharField(min_length=6)
    re_password = forms.CharField(min_length=6)
    def clean_username(self):
        username=self.cleaned_data.get('username')
        if username_check(username):
            filter_result = User.objects.filter(username=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("username already taken.")
            return username
        else:
            raise forms.ValidationError("username has illegal characters.")

    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if len(tel) = 11:
            return password
        else:
            raise forms.ValidationError("Your must input 11 bit phone number.")
        return password
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("password too short.")
        elif len(password) > 20:
            raise forms.ValidationError("Your password is too long.")
        return password

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('confirm')
        if password and re_password and password != re_password:
            raise forms.ValidationError("Password mismatch.")
        return re_password