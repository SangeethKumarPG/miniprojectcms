from django.urls import path
from .views import *
urlpatterns = [
    path('facultylist/',get_faculty_list, name="facultylist"),
    path('internalmark/template',export_csv_template, name="get_template"),
    path('internalmark/bulkupload',populate_student_semester, name="bulk_upload")
]