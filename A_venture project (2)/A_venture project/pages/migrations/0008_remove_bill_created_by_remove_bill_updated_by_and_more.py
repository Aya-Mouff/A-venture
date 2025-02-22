# Generated by Django 5.0.4 on 2025-01-08 21:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0007_bill_created_by_bill_updated_by_user_groups_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bill",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="bill",
            name="updated_by",
        ),
        migrations.RemoveField(
            model_name="user",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_superuser",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_login",
        ),
        migrations.RemoveField(
            model_name="user",
            name="user_permissions",
        ),
    ]
