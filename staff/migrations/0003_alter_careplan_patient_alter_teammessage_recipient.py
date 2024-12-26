# Generated by Django 5.1.4 on 2024-12-24 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_alter_emergencyservice_patient_and_more'),
        ('staff', '0002_alter_appointment_patient_alter_appointment_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careplan',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='care_plans', to='patients.patient'),
        ),
        migrations.AlterField(
            model_name='teammessage',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_received_messages', to='staff.staff'),
        ),
    ]
