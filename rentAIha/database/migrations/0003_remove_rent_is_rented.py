# Generated by Django 5.0.1 on 2024-01-30 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_iha_rename_is_superuser_user_is_admin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rent',
            name='is_rented',
        ),
    ]