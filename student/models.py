from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


import os
from uuid import uuid4



def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 17:
        raise ValidationError(_("You should be at least 17 years old to register"))

def validate_graduation_date(value):
    if value:
        today = date.today()
        year_gap = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if year_gap <= 0:
            raise ValidationError(_("Only graduated candidates are eligible for registration"))
        

def generate_filename(instance,filename):
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid4()}{ext}"
    return os.path.join("documents",new_filename)

def generate_photoname(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join("photos",filename)

class Stream(models.Model):
    name = models.CharField(max_length=100, validators=[RegexValidator(regex='^[A-Za-z\s]*$', message=_("Only alphabets allowed"))])
    def __str__(self):
        return self.name
    

class Course(models.Model):
    name = models.CharField(max_length=100, validators=[RegexValidator(regex='^[A-Za-z0-9]*$', message=_("Special characters not allowed"))])
    fee_structure = models.ForeignKey('FeeStructure', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self) -> str:
        return self.name
    
    
class Registration(models.Model):
    admission_number = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, validators=[RegexValidator(regex='^[A-Za-z\s]*$', message=_("Only alphabets allowed"))])
    last_name = models.CharField(max_length=100, validators=[RegexValidator(regex='^[A-Za-z\s]*$', message=_("Only alphabets allowed"))])
    course_option1 = models.ForeignKey(Course, related_name='course_option1_registrations', on_delete=models.CASCADE)
    course_option2 = models.ForeignKey(Course, related_name='course_option2_registrations', on_delete=models.CASCADE)
    admission_date = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(null=False, blank=False, validators=[validate_age])
    graduation_date = models.DateField(null=False, blank=False, validators=[validate_graduation_date])
    graduation_stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    graduation_percentage = models.FloatField(
        validators=[RegexValidator(
            regex=r'^(?:100(?:\.0{1,2})?|99(?:\.[0-9]{1,2})?|9[0-8](?:\.[0-9]{1,2})?|(?:[5-8][0-9]|4[5-9])(?:\.[0-9]{1,2})?|50(?:\.00)?)$',
            message=_("Candidate should score at least 50%")
        )]
    )
    student_email = models.EmailField(null=False, blank=False)
    photo = models.ImageField(upload_to=generate_photoname, blank=False, null=False)
    roll_number = models.CharField(max_length=100, null=True, blank=True)
    selected_course = models.ForeignKey(Course, related_name='selected_course_registrations', on_delete=models.CASCADE, blank=True, null =True)
    graduation_certificate = models.FileField(upload_to=generate_filename, blank=True, null=True)
    transfer_certificate = models.FileField(upload_to=generate_filename,blank=True, null=True)
    IS_ADMITTED_CHOICES = [
        ('admitted', 'admitted'),
        ('pending', 'pending'),
        ('rejected', 'rejected'),
    ]
    guardian_name = models.CharField(max_length=100, validators=[RegexValidator(regex='^[A-Za-z\s]*$', message=_("Only alphabets allowed"))], null=True, blank=True)
    relationship_with_guardian = models.CharField(max_length=100, validators=[RegexValidator(regex='^[A-Za-z\s]*$', message=_("Only alphabets allowed"))], null=True, blank=True)
    contact_number_of_guardian = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^[0-9\s\+]*$', message=_("Invalid phone number"))], null=True, blank=True)
    first_semester_fee_paid = models.DateField(blank=True, null=True)
    second_semester_fee_paid = models.DateField(blank=True, null=True)
    third_semester_fee_paid = models.DateField(blank=True, null=True)
    fourth_semester_fee_paid = models.DateField(blank=True, null=True)
    admission_status = models.CharField(max_length=20, choices=IS_ADMITTED_CHOICES)
    edit_link_count = models.IntegerField(default=3)
    def __str__(self):
        return f"{self.admission_number}-{self.first_name}-{self.last_name}"
    





class FeeStructure(models.Model):
    first_semester=models.FloatField(blank=True, null=True)
    second_semester=models.FloatField(blank=True, null=True)
    third_semester=models.FloatField(blank=True, null=True)
    fourth_semester=models.FloatField(blank=True, null=True)
   



