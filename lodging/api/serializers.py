import string
from rest_framework import serializers
from lodging.models import Stays, StayImage
from urllib.request import urlopen
import json
from geopy.distance import geodesic
import geocoder


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
            url = "http://ipinfo.io/json"
            response = urlopen(url)
            data = json.load(response)
            ip = data["ip"]

        return ip

    def get_user_distance(self, obj):
        ip = self.get_user_ip(self.context["request"])
        # loc = geocoder.ipinfo(ip)
        # loc = loc.latlng

        # latitiude = loc[0]
        # longitute = loc[1]

        # user_loc = (latitiude, longitute)
        # stay_loc = (obj.latitude, obj.longitude)

        # return geodesic(user_loc, stay_loc).km

        return ip
