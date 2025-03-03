# Generated by Django 5.1.6 on 2025-02-21 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.TextField()),
                ('wilaya', models.TextField()),
                ('field', models.TextField()),
                ('activity', models.TextField()),
                ('description', models.DateField()),
                ('label', models.CharField(choices=[('accepted', 'accepted'), ('rejected', 'rejected')], max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.RemoveField(
            model_name='bill',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='billservice',
            name='bill',
        ),
        migrations.RemoveField(
            model_name='billservice',
            name='service',
        ),
        migrations.RemoveField(
            model_name='chroniccondition',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='inheritedillness',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='medicationprescription',
            name='medication',
        ),
        migrations.RemoveField(
            model_name='medicationprescription',
            name='prescription',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='progressnote',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='report',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='progressnote',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='report',
            name='generated_by',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin')], max_length=12),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('blocked', 'Blocked')], max_length=12),
        ),
        migrations.DeleteModel(
            name='Allergy',
        ),
        migrations.DeleteModel(
            name='Bill',
        ),
        migrations.DeleteModel(
            name='BillService',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.DeleteModel(
            name='ChronicCondition',
        ),
        migrations.DeleteModel(
            name='InheritedIllness',
        ),
        migrations.DeleteModel(
            name='Medication',
        ),
        migrations.DeleteModel(
            name='MedicationPrescription',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
        migrations.DeleteModel(
            name='Prescription',
        ),
        migrations.DeleteModel(
            name='ProgressNote',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]
