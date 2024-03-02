from django.apps import AppConfig
from django.db.models.signals import pre_save

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self) -> None:
        from .signals import send_email_notification
        from .models import BlogPost
        pre_save.connect(send_email_notification, sender=BlogPost)