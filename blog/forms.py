from .models import BlogPost
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BlogForm(forms.ModelForm):
    body=forms.CharField(widget=CKEditorUploadingWidget(config_name="default"))

    class Meta:
        model = BlogPost
        fields = ['title','body','category']
        