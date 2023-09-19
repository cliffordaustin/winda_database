from .models import CustomUser

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


admin.site.site_header = "Winda Administration"

admin.site.site_url = "https://winda-guide.vercel.app/"


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        exclude = []

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        exclude = []

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("first_name", "last_name", "primary_email", "is_admin")
    list_filter = ("is_admin", "is_superuser")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "primary_email",
                    "password",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Personal info",
            {"fields": ["profile_pic", "instagram_username", "tiktok_username"]},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "email_verified",
                    "is_admin",
                    "is_staff",
                    "is_partner",
                    "is_agent",
                    "is_superuser",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "instagram_username",
                    "tiktok_username",
                    "email",
                    "primary_email",
                    "profile_pic",
                    "password1",
                    "password2",
                    "email_verified",
                    "is_admin",
                    "is_partner",
                    "is_agent",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email", "primary_email", "first_name", "last_name")
    ordering = ("email", "primary_email", "first_name", "last_name", "email_verified")
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)

admin.site.unregister(Group)
