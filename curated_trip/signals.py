from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import *
from django.utils.text import slugify
from core.utils import generate_random_string

# curated trips signals
@receiver(pre_save, sender=CuratedTrip)
def create_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=StayTrip)
def create_stay_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=ActivityTrip)
def create_experience_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=TransportationTrip)
def create_transport_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


# user trip signals
@receiver(pre_save, sender=UserTrip)
def create_user_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=UserTrips)
def create_user_trips_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=UserStayTrip)
def create_user_stay_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=UserActivityTrip)
def create_user_experience_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=UserTransportTrip)
def create_user_transport_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string
