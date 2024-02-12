# Generated by Django 4.2.9 on 2024-02-11 14:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import student.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Special characters not allowed', regex='^[A-Za-z0-9]*$')])),
            ],
        ),
        migrations.CreateModel(
            name='FeeStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_semester', models.FloatField(blank=True, null=True)),
                ('second_semester', models.FloatField(blank=True, null=True)),
                ('third_semester', models.FloatField(blank=True, null=True)),
                ('fourth_semester', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Only alphabets allowed', regex='^[A-Za-z]*$')])),
                ('relationship', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Only alphabets allowed', regex='^[A-Za-z]*$')])),
                ('contact_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Invalid phone number', regex='^[+-]?\\d+$')])),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Only alphabets allowed', regex='^[A-Za-z]*$')])),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('admission_number', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Only alphabets allowed', regex='^[A-Za-z]*$')])),
                ('last_name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Only alphabets allowed', regex='^[A-Za-z]*$')])),
                ('admission_date', models.DateField(blank=True, null=True)),
                ('date_of_birth', models.DateField(validators=[student.models.validate_age])),
                ('graduation_date', models.DateField(validators=[student.models.validate_graduation_date])),
                ('graduation_percentage', models.FloatField(validators=[django.core.validators.RegexValidator(message='Candidate should score at least 50%', regex='^(?:100(?:\\.0{1,2})?|99(?:\\.[0-9]{1,2})?|9[0-8](?:\\.[0-9]{1,2})?|(?:[5-8][0-9]|4[5-9])(?:\\.[0-9]{1,2})?|50(?:\\.00)?)$')])),
                ('student_email', models.EmailField(max_length=254)),
                ('photo', models.ImageField(upload_to=student.models.generate_photoname)),
                ('roll_number', models.CharField(blank=True, max_length=100, null=True)),
                ('graduation_certificate', models.FileField(blank=True, null=True, upload_to=student.models.generate_filename)),
                ('transfer_certificate', models.FileField(blank=True, null=True, upload_to=student.models.generate_filename)),
                ('first_semester_fee_paid', models.DateField(blank=True, null=True)),
                ('second_semester_fee_paid', models.DateField(blank=True, null=True)),
                ('third_semester_fee_paid', models.DateField(blank=True, null=True)),
                ('fourth_semester_fee_paid', models.DateField(blank=True, null=True)),
                ('admission_status', models.CharField(choices=[('admitted', 'admitted'), ('pending', 'pending'), ('rejected', 'rejected')], max_length=20)),
                ('course_option1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_option1_registrations', to='student.course')),
                ('course_option2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_option2_registrations', to='student.course')),
                ('graduation_stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.stream')),
                ('guardian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.guardian')),
                ('selected_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_course_registrations', to='student.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='fee_structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.feestructure'),
        ),
    ]
