# Generated by Django 5.1.6 on 2025-02-21 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_record_remove_bill_doctor_remove_bill_patient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='description',
            field=models.TextField(),
        ),
    ]
