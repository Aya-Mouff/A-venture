# Generated by Django 5.0.4 on 2025-01-10 22:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0009_appointment"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Appointment",
        ),
    ]
