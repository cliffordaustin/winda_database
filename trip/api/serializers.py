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
        instance.activity_from_date = validated_data.get(
            "activity_from_date", instance.activity_from_date
        )
        instance.to_date = validated_data.get("to_date", instance.to_date)
        instance.nights = validated_data.get("nights", instance.nights)
        instance.number_of_people = validated_data.get(
            "number_of_people", instance.number_of_people
        )
        instance.user_need_a_driver = validated_data.get(
            "user_need_a_driver", instance.user_need_a_driver
        )
        instance.number_of_days = validated_data.get(
            "number_of_days", instance.number_of_days
        )

        instance.save()
        return instance


class GroupTripSerializer(serializers.ModelSerializer):
    trip = TripSerializer(read_only=True, many=True)
    user = serializers.StringRelatedField(read_only=True)
    transport_back = TransportSerializer(read_only=True)
    transport_id = serializers.PrimaryKeyRelatedField(
        queryset=Transportation.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = GroupTrip
        fields = "__all__"
        depth = 1

    def update(self, instance, validated_data):
        instance.transport_back = validated_data.get(
            "transport_id", instance.transport_back
        )
        instance.starting_point = validated_data.get(
            "starting_point", instance.starting_point
        )
        instance.paid = validated_data.get("paid", instance.paid)
        instance.save()

        return instance