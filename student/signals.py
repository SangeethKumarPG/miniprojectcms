
from .models import Registration
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
import string

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