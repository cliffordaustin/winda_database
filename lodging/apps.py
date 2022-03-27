from django.apps import AppConfig


class LodgingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lodging"

    def ready(self):
        import lodging.signals
