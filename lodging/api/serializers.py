import string
from rest_framework import serializers
from activities.api.serializers import ActivitySerializer
from activities.models import Activities
from lodging.models import *
from urllib.request import urlopen
import json
from geopy.distance import geodesic
import geocoder
import socket
from ipware import get_client_ip
import whatismyip
import requests
from lodging.models import Review
from activities.models import Review as ActivityReview
from django.db.models import Sum

from transport.api.serializers import TransportSerializer
from transport.models import Transportation


class StayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StayImage
        exclude = ["stay"]


class ExperiencesIncludedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperiencesIncluded
        exclude = ["stay"]


class FactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facts
        exclude = ["stay"]


class InclusionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inclusions
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
    experiences_included = ExperiencesIncludedSerializer(many=True, read_only=True)
    facts = FactsSerializer(many=True, read_only=True)
    inclusions = InclusionsSerializer(many=True, read_only=True)

    has_user_saved = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()

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

    def get_saved_count(self, instance):
        return instance.saved_stays.count()

    def get_has_user_saved(self, instance):
        request = self.context.get("request")

        try:
            saved = SaveStays.objects.filter(stay=instance, user=request.user)
            saved = saved.exists()
        except:
            saved = False
        return saved

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


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay = StaysSerializer(read_only=True)
    user_has_reviewed_stay = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_user_has_reviewed_stay(self, instance):
        request = self.context.get("request")

        order_review = Review.objects.filter(stay=instance.stay, user=request.user)

        return order_review.exists()


class SaveStaysSerializer(serializers.ModelSerializer):
    stay = StaysSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SaveStays
        fields = "__all__"
