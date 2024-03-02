from django.db import models
from django.core.validators import RegexValidator
from student.models import Course
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.

def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 22:
        raise ValidationError(_("You should be at least 22 years old to register"))


class Faculty(models.Model):
    first_name = models.CharField(max_length=100, validators=[RegexValidator(regex='^[A-Za-z]*$', message=_("Only alphabets allowed"))])
    last_name = models.CharField(max_length=100, validators=[RegexValidator(regex='^[A-Za-z]*$', message=_("Only alphabets allowed"))])
    co_ordinator = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    dob = models.DateField(validators=[validate_age], blank=False, null=False)
    highest_qualification = models.CharField(max_length=100, validators=[RegexValidator(regex='^[a-zA-Z0-9.]*$', message=_("Invalid Qualification. Must not have special characters"))])
    years_of_experience = models.FloatField(blank=False, null=False)
    email = models.EmailField(null=True, blank=True)
    def __str__(self) -> str:
        return self.first_name+self.last_name