from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyBaseUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', max_length=18, min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = MyBaseUser
        fields = ('right',)

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # here set current time to created_date
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
            'fields': ( 'password', 'right')}
         ),
    )
    search_fields = ('id',)
    ordering = ('id',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(MyBaseUser, UserAdmin)
admin.site.unregister(Group)