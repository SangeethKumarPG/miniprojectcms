from .models import BlogPost
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
import string
from .email_handler import *

@receiver(pre_save, sender=BlogPost)
def send_email_notification(sender, instance, **kwargs):
    print("Inside presave")
    if instance.pk is None:
        if instance.category == "general":
            send_mail_to_all(instance.title)
        elif instance.category =="administrative":
            send_email_to_staff(instance.title)

    elif instance.category=="general" and instance.pk is not None:
        send_mail_to_all(instance.title, pk=instance.pk)
    elif instance.category =="administrative" and instance.pk is not None:
        send_email_to_staff(instance.title, pk=instance.pk)
    else:
        pass