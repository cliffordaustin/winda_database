import string
from rest_framework import serializers
from lodging.models import Cart, Stays, StayImage, Views
from urllib.request import urlopen
import json
from geopy.distance import geodesic
import geocoder
import socket
from ipware import get_client_ip
import whatismyip
import requests
from lodging.models import Review
from django.db.models import Sum


class StayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StayImage
        exclude = ["stay"]


class StaysSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay_images = StayImageSerializer(many=True, read_only=True)
    is_user_stay = serializers.SerializerMethodField()
    has_user_reviewed = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    num_of_five_stars = serializers.SerializerMethodField()
    num_of_four_stars = serializers.SerializerMethodField()
    num_of_three_stars = serializers.SerializerMethodField()
    num_of_two_stars = serializers.SerializerMethodField()
    num_of_one_stars = serializers.SerializerMethodField()
    total_num_of_reviews = serializers.SerializerMethodField()
    count_total_review_rates = serializers.SerializerMethodField()

    def get_count_total_review_rates(self, instance):
        return instance.reviews.aggregate(Sum("rate"))["rate__sum"]

    def get_total_num_of_reviews(self, instance):
        return instance.reviews.count()

    def get_num_of_one_stars(self, instance):
        return instance.reviews.filter(rate=1).count()

    def get_num_of_two_stars(self, instance):
        return instance.reviews.filter(rate=2).count()

    def get_num_of_three_stars(self, instance):
        return instance.reviews.filter(rate=3).count()

    def get_num_of_four_stars(self, instance):
        return instance.reviews.filter(rate=4).count()

    def get_num_of_five_stars(self, instance):
        return instance.reviews.filter(rate=5).count()

    class Meta:
        model = Stays
        fields = "__all__"

    def get_is_user_stay(self, instance):
        request = self.context.get("request")
        try:
            is_user = True if instance.user == request.user else False
        except:
            is_user = False
        return is_user

    def get_views(self, instance):
        return instance.views.count()

    def get_has_user_reviewed(self, instance):
        request = self.context.get("request")
        try:
            has_user_reviewed = (
                True if instance.reviews.filter(user=request.user).exists() else False
            )
        except:
            has_user_reviewed = False
        return has_user_reviewed


class StayViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Views
        exclude = ["stay"]


class CartSerializer(serializers.ModelSerializer):
    stay = StaysSerializer(read_only=True)

    class Meta:
        model = Cart
        exclude = ["user"]
        read_only_fields = ("ordered",)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    name = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    date_posted = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ["stay"]

    def get_name(self, instance):
        return (
            f"{instance.user.first_name} {instance.user.last_name}"
            if instance.user.first_name or instance.user.last_name
            else instance.user.email
        )

    def get_profile_pic(self, instance):
        return instance.user.profile_pic.url if instance.user.profile_pic else None
