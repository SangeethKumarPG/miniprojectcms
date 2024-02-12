from django.urls import path
from .views import *
urlpatterns = [
    path("form/",RegistrationCreateView.as_view(), name="registration_form"),
]