from rest_framework import serializers
from lodging.models import Stays, StayImage
from urllib.request import urlopen
import json
from geopy.distance import geodesic


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
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def get_user_distance(self, obj):
        url = "http://ipinfo.io/json"
        response = urlopen(url)
        data = json.load(response)
        loc = data["loc"]

        location = loc.split(",")

        latitiude = float(location[0])
        longitute = float(location[1])

        user_loc = (latitiude, longitute)
        stay_loc = (obj.latitude, obj.longitude)

        return loc

        # return geodesic(user_loc, stay_loc).km

        # ip = self.get_user_ip(self.context["request"])

        # return ip
