from django.urls import path
from .views import *
urlpatterns = [
    path('facultylist/',get_faculty_list, name="facultylist"),
]