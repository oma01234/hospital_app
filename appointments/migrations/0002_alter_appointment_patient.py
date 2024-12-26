# Generated by Django 5.1.4 on 2024-12-22 21:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
        ('patients', '0003_profile_next_of_kin_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_patient', to='patients.patient'),
        ),
    ]