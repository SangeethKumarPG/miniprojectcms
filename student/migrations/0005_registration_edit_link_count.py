# Generated by Django 4.2.9 on 2024-03-02 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_alter_registration_selected_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='edit_link_count',
            field=models.IntegerField(default=3),
        ),
    ]
