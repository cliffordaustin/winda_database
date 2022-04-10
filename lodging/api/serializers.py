from rest_framework import serializers
from lodging.models import Stays, StayImage
import socket


class StayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StayImage
        exclude = ["stay"]


class StaysSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay_images = StayImageSerializer(many=True, read_only=True)
    user_distance = serializers.SerializerMethodField()

    class Meta:
        model = Stays
        fields = "__all__"

    def get_user_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[-1].strip()
            print("First")
        else:
            ip = request.META.get("REMOTE_ADDR")
            print("Second")
        return ip

        # hostname = socket.gethostname()
        # ip_address = socket.gethostbyname(hostname)

        # return ip_address

    def get_user_distance(self, obj):
        user_ip = self.get_user_ip(self.context["request"])
        return user_ip


# class UserLocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserLocation
#         exclude = ["stay"]
