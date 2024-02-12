from django.shortcuts import render
from .models import Faculty
# Create your views here.

def get_faculty_list(request):
    faculties = Faculty.objects.all()
    return render(request,template_name="faculty_list.html", context={"faculties":faculties})