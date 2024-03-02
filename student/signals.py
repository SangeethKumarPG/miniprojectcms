
from .models import Registration
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
import requests

from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
import string

EMAIL_LINK_BASE ="http://127.0.0.1:8000/"
EMAIL_VALIDATION_URL = "https://emailvalidation.abstractapi.com/v1/?api_key=dc21d7f41bf74b0bb990e7fea8bb3b53"

@receiver(pre_save, sender=Registration)
def generate_roll_number(sender, instance, **kwargs):
    print("Inside presave")
    print(instance.admission_status)
    print(f"instance.roll_number == '' : {not instance.roll_number}")
    if instance.pk is None:  
        print("Primary key none")
        if instance.admission_status == 'admitted':
            latest_instance = Registration.objects.filter(admission_status='admitted').order_by('-roll_number').first()
            if latest_instance:
                print("latest instance")
                latest_roll_number = latest_instance.roll_number
                num_part = int(latest_roll_number[3:]) + 1
                if num_part <= 999:
                    new_roll_number = f'{latest_roll_number[:3]}{num_part:03d}' 
                    instance.roll_number = new_roll_number
                else:
                    char_seq = string.ascii_uppercase[string.ascii_uppercase.index(latest_roll_number[0]) + 1]
                    instance.roll_number = f'{char_seq}BA001'
            else:
                print("New instance")
                instance.roll_number = 'AAA001'
        else:
            print("Set empty roll number")
            instance.roll_number = ''
    elif instance.admission_status == 'admitted' and not instance.roll_number:
        print("admitted with no roll number")
        latest_instance = Registration.objects.filter(admission_status='admitted').order_by('-roll_number').first()
        if latest_instance:
            print("Admitted latest instance no roll number")
            latest_roll_number = latest_instance.roll_number
            num_part = int(latest_roll_number[3:]) + 1
            if num_part <= 999:
                new_roll_number = f'{latest_roll_number[:3]}{num_part:03d}' 
                instance.roll_number = new_roll_number
            else:
                char_seq = string.ascii_uppercase[string.ascii_uppercase.index(latest_roll_number[0]) + 1]
                instance.roll_number = f'{char_seq}BA001'
        else:
            print("Admitted initialize first roll number")
            instance.roll_number = 'AAA001'
        print("Add admission time")
        instance.admission_date = timezone.now().date()
        # if validate_email(instance.student_email):
        #     send_mail(
        #         subject=f"Admission Process of {instance.first_name} {instance.last_name} completed",
        #         message=f"Congratulations!!! Your admission for {instance.selected_course} has been completed. Your roll number is:{instance.roll_number}",
        #         from_email=settings.EMAIL_HOST_USER,
        #         recipient_list=[instance.student_email],
        #         fail_silently=True
        #     )



def is_valid_email(data):
    print(data)
    print(data['deliverability'])
    print(data['is_valid_format']["value"])
    if data['deliverability'] =="DELIVERABLE" and data['is_valid_format']["value"]:
        return True
    
    return False

def validate_email(email):
    response = requests.get(EMAIL_VALIDATION_URL + "&email=" + email)
    if response.status_code == 200:
        print(response.url)
        result = response.json()
        if is_valid_email(result):
            return True
    else:
        print(f"Error validating email {email}: HTTP status code {response.status_code}")
        return False

@receiver(post_save, sender=Registration)
def send_registraion_email(sender, instance, created, **kwargs):
    if created:
        subject="Admission Registration Completed"
        message=f'Hello {instance.first_name} {instance.last_name} \n\n your have succesfully completed the first step of registraion.'
        edit_link = reverse('registraion_update',kwargs={'pk':instance.pk})
        message+=f"You can edit the submitted details by using this link: {EMAIL_LINK_BASE}{edit_link}"

        if validate_email(instance.student_email):
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.student_email],
                fail_silently=True
            )
    else:
        if instance.edit_link_count <= 3 and instance.edit_link_count >= 0:
            current_link_count = instance.edit_link_count
            current_link_count -= 1
            instance.edit_link_count = current_link_count
            subject="Admission Registration Completed"
        message=f'Hello {instance.first_name} {instance.last_name} \n\n your have succesfully completed the first step of registraion.'
        edit_link = reverse('registraion_update',kwargs={'pk':instance.pk})
        message+=f"You can edit the submitted details by using this link: {EMAIL_LINK_BASE}{edit_link}"

        if validate_email(instance.student_email):
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.student_email],
                fail_silently=True
            )


