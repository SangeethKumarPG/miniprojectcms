
from django.urls import path
from .views import index,contact
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('',index, name="index"),
    path('contact/',contact, name="contact"),
    path('logout/',auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    path("accounts/login/",LoginView.as_view(), name="login"),
]