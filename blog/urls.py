
from django.urls import path
from .views import *
urlpatterns = [
    path('newpost/',BlogPostCreateView.as_view(),name="newpost"),
    path('viewpost/',ShowPostListView.as_view(), name="showposts"),
]