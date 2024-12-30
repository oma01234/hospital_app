# Generated by Django 5.1.4 on 2024-12-30 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_remove_appointment_unique_staff_appointment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_appointments', to='staff.staff'),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Doctor_schedule', to='staff.staff'),
            preserve_default=False,
        ),
    ]
