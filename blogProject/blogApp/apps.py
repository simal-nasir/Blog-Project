from django.apps import AppConfig

class BlogAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogApp'

    def ready(self):
        import blogApp.signals  # Ensure signals are imported