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

        return geodesic(user_loc, stay_loc).km
