# Generated by Django 5.1.4 on 2024-12-30 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0006_alter_appointment_doctor'),
        ('staff', '0008_appointment_created_by_doctorschedule_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(limit_choices_to={'role': 'doctor'}, on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
    ]
