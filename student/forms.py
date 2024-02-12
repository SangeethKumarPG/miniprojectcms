from typing import Any
from django.forms import ModelForm
from .models import *
from django import forms
from django.core.validators import RegexValidator
class StudentRegistrationForm(ModelForm):
    class Meta:
        model=Registration
        fields=['first_name', 'last_name',
                'course_option1', 'course_option2', 
                'date_of_birth',
                'graduation_date', 'graduation_stream',
                'graduation_percentage',
                'guardian_name','relationship_with_guardian','contact_number_of_guardian',
                'student_email', 'photo',
                'graduation_certificate', 'transfer_certificate',
                ]
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course_option1'].queryset = Course.objects.all()
        self.fields['course_option2'].queryset = Course.objects.all()
        self.fields['graduation_stream'].queryset = Stream.objects.all()
        # self.fields['guardian'].queryset = Guardian.objects.all()
        self.fields['date_of_birth'].widget = forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        )
        self.fields['graduation_date'].widget = forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        )
