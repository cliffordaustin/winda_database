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

from user.api.serializer import UserSerializer

from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)


class StayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StayImage
        exclude = ["stay"]


class ExtrasIncludedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtrasIncluded
        exclude = ["stay"]


class FactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facts
        exclude = ["stay"]


class InclusionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inclusions
        exclude = ["stay"]


class TypeOfRoomsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfRoomsImages
        exclude = ["room"]


class TypeOfRoomsSerializer(serializers.ModelSerializer):
    type_of_room_images = TypeOfRoomsImagesSerializer(many=True, read_only=True)

    class Meta:
        model = TypeOfRooms
        exclude = ["stay"]


class PrivateSafariImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateSafariImages
        exclude = ["private_safari"]


class PrivateSafariSerializer(serializers.ModelSerializer):
    private_safari_images = PrivateSafariImagesSerializer(many=True, read_only=True)

    class Meta:
        model = PrivateSafari
        exclude = ["stay"]


class AllInclusiveImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllInclusiveImages
        exclude = ["all_inclusive"]


class AllInclusiveSerializer(serializers.ModelSerializer):
    all_inclusive_images = AllInclusiveImagesSerializer(many=True, read_only=True)

    class Meta:
        model = AllInclusive
        exclude = ["stay"]


class OtherOptionImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherOptionImages
        exclude = ["other_option"]


class OtherOptionSerializer(serializers.ModelSerializer):
    other_option_images = OtherOptionImagesSerializer(many=True, read_only=True)

    class Meta:
        model = OtherOption
        exclude = ["stay"]


class SharedSafariImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedSafariImages
        exclude = ["shared_safari"]


class SharedSafariSerializer(serializers.ModelSerializer):
    shared_safari_images = SharedSafariImagesSerializer(many=True, read_only=True)

    class Meta:
        model = SharedSafari
        exclude = ["stay"]


class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        exclude = ["room_type"]


class RoomAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAvailability
        exclude = ["room_type"]


class RoomAvailabilityResidentGuestSerializer(
    BulkSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = RoomAvailabilityResidentGuest
        list_serializer_class = BulkListSerializer
        exclude = ["room_availability_resident"]


class ResidentOtherFeesSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ResidentOtherFees
        list_serializer_class = BulkListSerializer
        exclude = ["room_availability_resident"]


class RoomAvailabilityResidentSerializer(
    BulkSerializerMixin, serializers.ModelSerializer
):
    room_resident_guest_availabilities = RoomAvailabilityResidentGuestSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = RoomAvailabilityResident
        list_serializer_class = BulkListSerializer
        exclude = ["room_type"]


class RoomAvailabilityNonResidentGuestSerializer(
    BulkSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = RoomAvailabilityNonResidentGuest
        list_serializer_class = BulkListSerializer
        exclude = ["room_availability_non_resident"]


class NonResidentOtherFeesSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = NonResidentOtherFees
        list_serializer_class = BulkListSerializer
        exclude = ["room_availability_non_resident"]


class RoomAvailabilityNonResidentSerializer(
    BulkSerializerMixin, serializers.ModelSerializer
):
    room_non_resident_guest_availabilities = RoomAvailabilityNonResidentGuestSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = RoomAvailabilityNonResident
        list_serializer_class = BulkListSerializer
        exclude = ["room_type"]


class OtherFeesResidentSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = OtherFeesResident
        list_serializer_class = BulkListSerializer
        exclude = ["stay"]


class OtherFeesNonResidentSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = OtherFeesNonResident
        list_serializer_class = BulkListSerializer
        exclude = ["stay"]


class ParkFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkFees
        exclude = ["stay"]


class ActivityFeesSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ActivityFee
        list_serializer_class = BulkListSerializer
        exclude = ["stay"]


class RoomTypeSerializer(serializers.ModelSerializer):
    room_availabilities = RoomAvailabilitySerializer(many=True, read_only=True)
    room_resident_availabilities = RoomAvailabilityResidentSerializer(
        many=True, read_only=True
    )
    room_non_resident_availabilities = RoomAvailabilityNonResidentSerializer(
        many=True, read_only=True
    )
    bookings = BookingsSerializer(many=True, read_only=True)

    class Meta:
        model = RoomType
        exclude = ["stay"]


class RoomTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        exclude = ["stay"]


class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Agents
        exclude = ["stay"]


class AgentByEmailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AgentsByEmail
        exclude = ["stay"]


class AgentDiscountRateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AgentDiscountRate
        exclude = ["stay"]


class PropertyAccessSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PropertyAccess
        exclude = ["stay"]


class PartnerStaySerializer(serializers.ModelSerializer):
    activity_fees = ActivityFeesSerializer(read_only=True, many=True)
    other_fees_resident = OtherFeesResidentSerializer(many=True, read_only=True)
    other_fees_non_resident = OtherFeesNonResidentSerializer(many=True, read_only=True)
    stay_images = StayImageSerializer(many=True, read_only=True)
    has_property_access = serializers.SerializerMethodField()

    class Meta:
        model = Stays
        fields = [
            "user",
            "id",
            "slug",
            "is_partner_property",
            "property_name",
            "location",
            "activity_fees",
            "other_fees_resident",
            "other_fees_non_resident",
            "stay_images",
            "lodge_price_data_pdf",
            "has_property_access",
        ]

    def get_has_property_access(self, instance):
        request = self.context.get("request")
        return (
            instance.property_access.filter(email=request.user.primary_email).exists()
            or instance.property_access.filter(email=request.user.email).exists()
            or instance.user == request.user
            or instance.agents_email.filter(email=request.user.email).exists()
            or instance.agent_access.filter(user=request.user, approved=True).exists()
        )


class LodgeStaySerializer(serializers.ModelSerializer):
    stay_images = StayImageSerializer(many=True, read_only=True)
    number_of_agents = serializers.SerializerMethodField()
    has_property_access = serializers.SerializerMethodField()

    class Meta:
        model = Stays
        fields = [
            "user",
            "id",
            "slug",
            "is_partner_property",
            "property_name",
            "location",
            "stay_images",
            "lodge_price_data_pdf",
            "number_of_agents",
            "has_property_access",
        ]

    def get_number_of_agents(self, instance):
        return instance.agent_access.count()

    def get_has_property_access(self, instance):
        request = self.context.get("request")
        return (
            instance.property_access.filter(email=request.user.primary_email).exists()
            or instance.property_access.filter(email=request.user.email).exists()
            or instance.user == request.user
            or instance.agents_email.filter(email=request.user.email).exists()
            or instance.agent_access.filter(user=request.user, approved=True).exists()
        )


class DetailStaySerializer(serializers.ModelSerializer):
    stay_images = StayImageSerializer(many=True, read_only=True)

    class Meta:
        model = Stays
        fields = [
            "user",
            "id",
            "slug",
            "property_name",
            "name",
            "location",
            "stay_images",
            "in_homepage",
            "has_options",
        ]


class LodgeStayWaitingForApprovalSerializer(serializers.ModelSerializer):
    stay_images = StayImageSerializer(many=True, read_only=True)
    agent_access_request_made = serializers.SerializerMethodField()
    agent_access_request_approved = serializers.SerializerMethodField()

    class Meta:
        model = Stays
        fields = [
            "user",
            "id",
            "slug",
            "is_partner_property",
            "property_name",
            "location",
            "stay_images",
            "lodge_price_data_pdf",
            "agent_access_request_made",
            "agent_access_request_approved",
        ]

    def get_agent_access_request_made(self, instance):
        return instance.agent_access.filter(user=self.context["request"].user).exists()

    def get_agent_access_request_approved(self, instance):
        return instance.agent_access.filter(
            user=self.context["request"].user, approved=True
        ).exists()


class DetailStayWithAmenitiesSerializer(serializers.ModelSerializer):
    stay_images = StayImageSerializer(many=True, read_only=True)
    private_safari = PrivateSafariSerializer(read_only=True)
    shared_safari = SharedSafariSerializer(read_only=True)
    all_inclusive = AllInclusiveSerializer(read_only=True)
    other_options = OtherOptionSerializer(read_only=True, many=True)
    extras_included = ExtrasIncludedSerializer(many=True, read_only=True)
    facts = FactsSerializer(many=True, read_only=True)
    inclusions = InclusionsSerializer(many=True, read_only=True)

    class Meta:
        model = Stays
        fields = [
            "user",
            "id",
            "slug",
            "country",
            "description",
            "unique_about_place",
            "city",
            "property_name",
            "other_options",
            "name",
            "location",
            "type_of_stay",
            "capacity",
            "rooms",
            "beds",
            "bathrooms",
            "tags",
            "longitude",
            "latitude",
            "in_homepage",
            "has_options",
            "stay_images",
            "extras_included",
            "other_options",
            "private_safari",
            "shared_safari",
            "all_inclusive",
            "facts",
            "inclusions",
            # Amenities
            "swimming_pool",
            "hot_tub",
            "sauna",
            "gym",
            "patio",
            "terrace",
            "balcony",
            "firepit",
            "barbecue_grill",
            "outdoor_dining_area",
            "spa",
            "wifi",
            "parking",
            "tv",
            "air_conditioning",
            "heating",
            "kitchen",
            "fridge",
            "laundry",
            "washing_machine",
            "dedicated_working_area",
            "smoke_alarm",
            "first_aid_kit",
            "medical_service_on_site",
            "carbon_monoxide_detector",
            "lockable_room",
            "bar",
            "restaurant",
            "giftshop",
            "photography_room",
            "themed_room",
            "pet_friendly",
            "barber_shop",
            "beauty_salon",
            "purified_drinking_water",
            "firewood",
            "conference_center",
            "ensuite_room",
            "library",
        ]


class StaysSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay_images = StayImageSerializer(many=True, read_only=True)
    type_of_rooms = TypeOfRoomsSerializer(many=True, read_only=True)
    room_types = RoomTypeSerializer(many=True, read_only=True)
    other_fees_resident = OtherFeesResidentSerializer(many=True, read_only=True)
    other_fees_non_resident = OtherFeesNonResidentSerializer(many=True, read_only=True)
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
    private_safari = PrivateSafariSerializer(read_only=True)
    shared_safari = SharedSafariSerializer(read_only=True)
    all_inclusive = AllInclusiveSerializer(read_only=True)
    other_options = OtherOptionSerializer(read_only=True, many=True)
    activity_fees = ActivityFeesSerializer(read_only=True, many=True)
    extras_included = ExtrasIncludedSerializer(many=True, read_only=True)
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


class LodgePackageBookingSerializer(serializers.ModelSerializer):
    stay = StaysSerializer(read_only=True)

    class Meta:
        model = LodgePackageBooking
        fields = "__all__"


class LodgePackageBookingInstallmentSerializer(serializers.ModelSerializer):
    stay = StaysSerializer(read_only=True)

    class Meta:
        model = LodgePackageBookingInstallment
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay = StaysSerializer(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"


class EventTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTransport
        fields = "__all__"


class SaveStaysSerializer(serializers.ModelSerializer):
    stay = StaysSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SaveStays
        fields = "__all__"
