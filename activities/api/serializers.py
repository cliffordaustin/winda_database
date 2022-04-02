from rest_framework import serializers
from activities.models import Activities, ActivitiesImage


class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        exclude = ["stay"]


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay_images = ActivityImageSerializer(many=True, read_only=True)

    class Meta:
        model = ActivitiesImage
        fields = "__all__"
