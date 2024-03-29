# Generated by Django 4.2.9 on 2024-02-03 16:16

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Blog Title')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('author', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
