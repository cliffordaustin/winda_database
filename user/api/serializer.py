from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from user.models import CustomUser
from mixpanel import Mixpanel

import os

mp = Mixpanel(os.environ.get("WINDA_MIXPANEL_TOKEN"))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "profile_pic",
            "avatar_url",
            "instagram_username",
            "tiktok_username",
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
            "avatar_url": self.validated_data.get("avatar_url", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        if self.cleaned_data.get("profile_pic"):
            user.profile_pic = self.cleaned_data.get("profile_pic")
        setup_user_email(request, user, [])
        user.save()

        mp.alias(user.email, user.email)

        mp.people_set(
            user.email,
            {
                "$email": user.email,
                "$first_name": user.first_name,
                "$last_name": user.last_name,
            },
        )
        return user
