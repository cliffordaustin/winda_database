from rest_framework import serializers
from transport.models import *
from django.db.models import Sum


class TransportImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationImage
        exclude = ["transportation"]


class TransportSerializer(serializers.ModelSerializer):
    transportation_images = TransportImagesSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    is_user_transport = serializers.SerializerMethodField()
    has_user_reviewed = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    num_of_five_stars = serializers.SerializerMethodField()
    num_of_four_stars = serializers.SerializerMethodField()
    num_of_three_stars = serializers.SerializerMethodField()
    num_of_two_stars = serializers.SerializerMethodField()
    num_of_one_stars = serializers.SerializerMethodField()
    total_num_of_reviews = serializers.SerializerMethodField()
    count_total_review_rates = serializers.SerializerMethodField()

    has_user_saved = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()

    def get_count_total_review_rates(self, instance):
        return instance.transport_review.aggregate(Sum("rate"))["rate__sum"]

    def get_total_num_of_reviews(self, instance):
        return instance.transport_review.count()

    def get_num_of_one_stars(self, instance):
        return instance.transport_review.filter(rate=1).count()

    def get_num_of_two_stars(self, instance):
        return instance.transport_review.filter(rate=2).count()

    def get_num_of_three_stars(self, instance):
        return instance.transport_review.filter(rate=3).count()

    def get_num_of_four_stars(self, instance):
        return instance.transport_review.filter(rate=4).count()

    def get_num_of_five_stars(self, instance):
        return instance.transport_review.filter(rate=5).count()

    def get_views(self, instance):
        return instance.transport_views.count()

    def get_saved_count(self, instance):
        return instance.saved_transport.count()

    def get_has_user_saved(self, instance):
        request = self.context.get("request")

        try:
            saved = SaveTransportation.objects.filter(
                transport=instance, user=request.user
            )
            saved = saved.exists()
        except:
            saved = False
        return saved

    def get_has_user_reviewed(self, instance):
        request = self.context.get("request")
        try:
            has_user_reviewed = (
                True
                if instance.transport_review.filter(user=request.user).exists()
                else False
            )
        except:
            has_user_reviewed = False
        return has_user_reviewed

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

    class Meta:
        model = Order
        fields = "__all__"

    def get_user_has_reviewed(self, instance):
        request = self.context.get("request")

        order_review = Review.objects.filter(
            transport=instance.transport, user=request.user
        )

        return order_review.exists()


class SaveTransportSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SaveTransportation
        fields = "__all__"
