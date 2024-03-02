from django.urls import path
from .views import *
urlpatterns = [
    path("form/",RegistrationCreateView.as_view(), name="registration_form"),
    path("form/<int:pk>", RegistrationUpdateView.as_view(), name="registraion_update"),
    path("payfees/", fee_payment, name="feepayment"),
    path("payfees/fetch-fees/",fetch_fee_detail, name="fee_details"),
    path("paymentsuccess/",payment_success),
    path("is-payment-succes",is_fee_paid, name="isfeepaid" )
]