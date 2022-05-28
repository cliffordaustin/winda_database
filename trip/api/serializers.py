from rest_framework import serializers
from trip.models import *
from lodging.models import *
from activities.models import *
from transport.models import *
from lodging.api.serializers import StaysSerializer
from activities.api.serializers import ActivitySerializer
from transport.api.serializers import TransportSerializer


class TripSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay = StaysSerializer(read_only=True)
    activity = ActivitySerializer(read_only=True)
    transport = TransportSerializer(read_only=True)

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
        model = Trip
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.transport = validated_data.get("transport_id", instance.transport)
        instance.activity = validated_data.get("activity_id", instance.activity)
        instance.stay = validated_data.get("stay_id", instance.stay)
        instance.from_date = validated_data.get("from_date", instance.from_date)
        instance.to_date = validated_data.get("to_date", instance.to_date)

        instance.save()
        return instance


class GroupTripSerializer(serializers.ModelSerializer):
    trip = TripSerializer(read_only=True, many=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GroupTrip
        fields = "__all__"
        depth = 1
