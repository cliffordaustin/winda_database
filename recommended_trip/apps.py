from django.apps import AppConfig


class RecommendedTripConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recommended_trip"

    def ready(self):
        import recommended_trip.signals
