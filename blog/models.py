from django.db import models

# Create your models here.

from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

class BlogPost(models.Model):
    title = models.CharField(
        _("Blog Title"), max_length=250,
        null=False, blank=False
    )
    body = RichTextUploadingField()
    author = models.CharField(max_length=100, blank=True, null=True)
    POST_CATEGORY = [
        ("general","general"),
        ("administrative","administrative"),
        ("miscellaneous","miscellaneous")
    ]
    category = models.CharField(max_length=100, choices=POST_CATEGORY, null=True, blank=True)
    publish_on = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title