# Generated by Django 4.2.9 on 2024-02-10 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='publish_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
