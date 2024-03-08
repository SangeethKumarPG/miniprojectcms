from django.contrib import admin

# Register your models here.
from .models import Stream, Course, Registration, FeeStructure, StudentSemester

admin.site.register(Stream)
admin.site.register(Course)

admin.site.register(Registration)
admin.site.register(FeeStructure)
admin.site.register(StudentSemester)