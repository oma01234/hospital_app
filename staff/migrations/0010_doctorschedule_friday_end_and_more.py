# Generated by Django 5.1.4 on 2024-12-30 12:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0009_alter_doctorschedule_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorschedule',
            name='friday_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='friday_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='monday_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='monday_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='saturday_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='saturday_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='sunday_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='sunday_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='thursday_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='thursday_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='tuesday_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='tuesday_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='wednesday_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='wednesday_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctorschedule',
            name='doctor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_schedule', to='staff.staff'),
        ),
    ]
