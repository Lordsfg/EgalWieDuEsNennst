from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):
        """
        Connect the signal receiver function when the app is ready.
        """
        from . import signals  # Import the signals module to ensure the signal handler is connected
