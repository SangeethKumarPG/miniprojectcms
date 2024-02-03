from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request=request,template_name='contact.html')