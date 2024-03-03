from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from .models import BlogPost
from .forms import BlogForm
from django.contrib import messages
from django.urls import reverse_lazy
import datetime
# Create your views here.

class BlogPostCreateView(LoginRequiredMixin,CreateView):
    model = BlogPost
    form_class = BlogForm
    template_name = "createblogpost.html"
    success_url = reverse_lazy('newpost')

    def form_valid(self, form):
        form.instance.author = self.request.user.username
        form.instance.publish_on = datetime.datetime.now()
        messages.success(self.request,"Post added Successfully!")
        return super().form_valid(form)
    
class ShowPostListView(ListView):
    model = BlogPost
    template_name="viewposts.html"
    context_object_name = "posts"
    paginate_by = 10
    def get_queryset(self) -> QuerySet[Any]:
        category=self.request.GET.get('category')
        if category:
            return BlogPost.objects.filter(category=category).order_by('-publish_on')
        else:
            return BlogPost.objects.all().order_by('-publish_on')



