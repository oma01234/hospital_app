# Generated by Django 5.1.4 on 2024-12-19 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treatmentplan',
            name='end_date',
        ),
    ]
