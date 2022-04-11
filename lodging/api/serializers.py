import string
from rest_framework import serializers
from lodging.models import Stays, StayImage
from urllib.request import urlopen
import json
from geopy.distance import geodesic
import geocoder
import socket
from ipware import get_client_ip
import whatismyip
import requests


class StayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StayImage
        exclude = ["stay"]


class StaysSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stay_images = StayImageSerializer(many=True, read_only=True)

    class Meta:
        model = Stays
        fields = "__all__"
