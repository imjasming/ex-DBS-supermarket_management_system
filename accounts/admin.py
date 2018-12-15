from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from accounts.models import MyBaseUser, Customer


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    a_username = forms.CharField(label='Username', max_length=20, min_length=6,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
                               error_messages={'required': 'username already taken.', })
    a_password = forms.CharField(label='Password', min_length=6, max_length=18,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    re_password = forms.CharField(label='Password confirmation', max_length=18, min_length=6,
                                  widget=forms.PasswordInput(
                                      attrs={'class': 'form-control', 'placeholder': 'confirm again'}))
    tel = forms.DecimalField(label='Phone number', max_digits=11,
                             widget=forms.NumberInput(
                                 attrs={'class': 'form-control', 'placeholder': 'you phone number'}))

    class Meta:
        model = MyBaseUser
        fields = ()

    def clean_a_username(self):
        a_username = self.cleaned_data.get('a_username')
        filter_result = MyBaseUser.objects.filter(username=a_username)
        if len(filter_result) > 0:
            raise forms.ValidationError("username already taken.")
        return a_username

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if len(password) < 6:
    #         raise forms.ValidationError("password too short.")
    #     elif len(password) > 20:
    #         raise forms.ValidationError("Your password is too long.")
    #     return password


    # def clean_re_password(self):
    #     password = self.cleaned_data.get('password')
    #     re_password = self.cleaned_data.get('confirm')
    #     if password and re_password and password != re_password:
    #         raise forms.ValidationError("Password mismatch.")
    #     return re_password

    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username',  'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password' )}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(MyBaseUser, UserAdmin)
admin.site.unregister(Group)
