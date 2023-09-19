from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from user.models import CustomUser
from mixpanel import Mixpanel
from django.conf import settings
from allauth.account.admin import EmailAddress
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

import os

mp = Mixpanel(os.environ.get("WINDA_MIXPANEL_TOKEN"))


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = [
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
            "created_at",
            "updated_at",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "instagram_username",
            "tiktok_username",
            "profile_pic",
            "is_partner",
            "is_agent",
            "avatar_url",
            "password1",
            "password2",
        ]

    @staticmethod
    def validate_email(email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address.",)
                )
        return email

    @staticmethod
    def validate_password1(password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                ("The two password fields didn't match.",)
            )
        return data

    def get_cleaned_data(self):
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "instagram_username": self.validated_data.get("instagram_username", ""),
            "tiktok_username": self.validated_data.get("tiktok_username", ""),
            "profile_pic": self.validated_data.get("profile_pic", ""),
            "is_partner": self.validated_data.get("is_partner", False),
            "is_agent": self.validated_data.get("is_agent", False),
            "avatar_url": self.validated_data.get("avatar_url", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request, invitation=False):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        if self.cleaned_data.get("profile_pic"):
            user.profile_pic = self.cleaned_data.get("profile_pic")
        user.is_partner = self.cleaned_data.get("is_partner")
        user.is_agent = self.cleaned_data.get("is_agent")
        user.set_password(self.cleaned_data.get("password1"))
        setup_user_email(request, user, [])
        user.save()

        if invitation:
            email_address = EmailAddress.objects.get(user=user)

            email_address.verified = True
            email_address.save()

        if settings.DEBUG is not True:
            mp.alias(user.email, user.email)

            mp.people_set(
                user.email,
                {
                    "$email": user.email,
                    "$first_name": user.first_name,
                    "$last_name": user.last_name,
                },
                meta={
                    "$ip": get_ip(request),
                },
            )

        return user
