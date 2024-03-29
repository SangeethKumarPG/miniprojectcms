# Generated by Django 4.2.9 on 2024-02-12 05:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_guardian_contact_number_alter_guardian_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='guardian',
        ),
        migrations.AddField(
            model_name='registration',
            name='contact_number_of_guardian',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Invalid phone number', regex='^[0-9\\s\\+]*$')]),
        ),
        migrations.AddField(
            model_name='registration',
            name='guardian_name',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator(message='Only alphabets allowed', regex='^[A-Za-z\\s]*$')]),
        ),
        migrations.AddField(
            model_name='registration',
            name='relationship_with_guardian',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator(message='Only alphabets allowed', regex='^[A-Za-z\\s]*$')]),
        ),
        migrations.DeleteModel(
            name='Guardian',
        ),
    ]
