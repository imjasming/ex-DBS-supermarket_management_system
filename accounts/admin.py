from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyBaseUser, Customer


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label='Username', max_length=20, min_length=6,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
                               error_messages={'required': 'username already taken.', })
    password = forms.CharField(label='Password', min_length=6, max_length=18,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    re_password = forms.CharField(label='Password confirmation', max_length=18, min_length=6,
                                  widget=forms.PasswordInput(
                                      attrs={'class': 'form-control', 'placeholder': 'confirm again'}))
    tel = forms.DecimalField(label='Phone number', max_digits=11,
                             widget=forms.NumberInput(
                                 attrs={'class': 'form-control', 'placeholder': 'you phone number'}))

    class Meta:
        model = Customer
        fields = ()

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'right', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('id', 'password', 'right')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password', 'right')}
         ),
    )
    search_fields = ('id',)
    ordering = ('id',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(MyBaseUser, UserAdmin)
admin.site.unregister(Group)
