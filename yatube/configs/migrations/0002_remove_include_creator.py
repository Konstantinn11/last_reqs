# Generated by Django 2.2.6 on 2022-07-29 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='include',
            name='creator',
        ),
    ]
