from django.apps import AppConfig


class CuratedTripConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "curated_trip"

    def ready(self):
        import curated_trip.signals
