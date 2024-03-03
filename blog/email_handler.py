
import requests
from student.models import Registration
from faculty.models import Faculty
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

EMAIL_VALIDATION_URL = "https://emailvalidation.abstractapi.com/v1/?api_key=dc21d7f41bf74b0bb990e7fea8bb3b53"
POST_URL = "http://127.0.0.1:8000/blog/viewpost/?pk="
# POST_URL = "http://127.0.0.1:8000/blog/viewpost/?pk="

def is_valid_email(data):
    print(data)
    print(data['deliverability'])
    print(data['is_valid_format']["value"])
    if data['deliverability'] =="DELIVERABLE" and data['is_valid_format']["value"]:
        return True
    
    return False

def validate_email(email_list):
    valid_emails = []
    for email in email_list:
        response = requests.get(EMAIL_VALIDATION_URL + "&email=" + email)
        if response.status_code == 200:
            print(response.url)
            result = response.json()
            if is_valid_email(result):
                valid_emails.append(email)
        else:
            print(f"Error validating email {email}: HTTP status code {response.status_code}")
    return valid_emails


def send_email(recipient_list, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list, fail_silently=True
    )



def send_mail_to_all(title, pk=None):
    less_than_two_years = timezone.now() - timedelta(days=365 * 2)
    # students = Registration.objects.filter(admission_date__lte=less_than_two_years)
    students = Registration.objects.all()
    validated_student_emails = []
    validated_staff_emails = []
    print(students)
    if students:
        email_ids = [student.student_email for student in students]
        validated_student_emails = validate_email(email_list=email_ids)

    staffs = Faculty.objects.all()
    if staffs:
        staff_emails = [staff.email for staff in staffs]
      
        staff_emails = [email for email in staff_emails if email is not None]
        if staff_emails:
            validated_staff_emails = validate_email(staff_emails)

    recipients = validated_student_emails + validated_staff_emails
    print(recipients)
    print(validated_student_emails)
    # print(email_ids)
    if pk is None:
        send_email(recipients, subject=f"Update: {title}", message=f"Dear User, You have a new notice")
    else:
        send_email(recipients, subject=f"Update: {title}", message=f"Dear User, You have a new notice. click the link to view {POST_URL+str(pk)}")

    


def send_email_to_staff(title, pk=None):
    staffs = Faculty.objects.all()
    validated_staff_email = []
    if staffs:
        staff_emails = [staff.email for staff in staffs]
        if staff_emails:
            validated_staff_email = validate_email(staff_emails)
    if pk is None:
        send_email(validated_staff_email, subject=f"Update: {title}", message=f"Dear User, You have a new notice")
    else:
        send_email(validated_staff_email, subject=f"Update: {title}", message=f"Dear User, You have a new notice. click the link to view {POST_URL+str(pk)}")