# Generated by Django 2.2.6 on 2023-02-13 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pro', '0005_auto_20230213_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event_type',
            name='block',
        ),
    ]
