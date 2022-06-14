from rest_framework import serializers
from recommended_trip.models import *
from lodging.api.serializers import StaysSerializer
from activities.api.serializers import ActivitySerializer
from transport.api.serializers import TransportSerializer


class SingleTripImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleTripImage
        fields = "__all__"


class TripSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay = StaysSerializer(read_only=True)
    activity = ActivitySerializer(read_only=True)
    transport = TransportSerializer(read_only=True)
    single_trip_images = SingleTripImageSerializer(many=True, read_only=True)

    stay_id = serializers.PrimaryKeyRelatedField(
        queryset=Stays.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    activity_id = serializers.PrimaryKeyRelatedField(
        queryset=Activities.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    transport_id = serializers.PrimaryKeyRelatedField(
        queryset=Transportation.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = SingleTrip
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.transport = validated_data.get("transport_id", instance.transport)
        instance.activity = validated_data.get("activity_id", instance.activity)
        instance.stay = validated_data.get("stay_id", instance.stay)

        instance.save()
        return instance
