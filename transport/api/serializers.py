from rest_framework import serializers
from transport.models import *


class TransportImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationImage
        exclude = ["transportation"]


class TransportSerializer(serializers.ModelSerializer):
    transportation_images = TransportImagesSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    is_user_transport = serializers.SerializerMethodField()

    class Meta:
        model = Transportation
        fields = "__all__"

    def get_is_user_transport(self, instance):
        request = self.context.get("request")
        try:
            is_user = True if instance.user == request.user else False
        except:
            is_user = False
        return is_user


class TransportViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Views
        exclude = ["transport"]


class CartSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(read_only=True)

    class Meta:
        model = Cart
        exclude = ["user"]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    name = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    date_posted = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ["transport"]

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
    transport = TransportSerializer(read_only=True)
    user_has_reviewed = serializers.SerializerMethodField()
    total_order_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_total_order_price(self, instance):
        return (instance.distance / 10) * instance.transport.price

    def get_user_has_reviewed(self, instance):
        request = self.context.get("request")

        order_review = Review.objects.filter(
            transport=instance.transport, user=request.user
        )

        return order_review.exists()
