# Generated by Django 4.2.9 on 2024-02-29 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_publish_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.CharField(blank=True, choices=[('general', 'general'), ('administrative', 'administrative'), ('miscellaneous', 'miscellaneous')], max_length=100, null=True),
        ),
    ]
