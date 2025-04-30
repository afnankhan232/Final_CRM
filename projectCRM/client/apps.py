from django.apps import AppConfig


class ClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client'

    # Registering the signal (for project -> [create DEFAULT])
    def ready(self):
        import client.signals