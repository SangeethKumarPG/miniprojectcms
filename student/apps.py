
from django.db.models.signals import pre_save, post_save
from django.apps import AppConfig

class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student'

    def ready(self):
        from .signals import generate_roll_number, send_registraion_email
        from .models import Registration
        pre_save.connect(generate_roll_number, sender=Registration)
        post_save.connect(send_registraion_email, sender=Registration)