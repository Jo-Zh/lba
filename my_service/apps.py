from django.apps import AppConfig


class MyServiceConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_service'

    def ready(self):
        import my_service.signals
