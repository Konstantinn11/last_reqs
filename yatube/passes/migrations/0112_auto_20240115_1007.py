# Generated by Django 2.2.6 on 2024-01-15 07:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0111_auto_20240115_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 1, 15, 10, 7, 19, 763661), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 15, 10, 7, 19, 762662), verbose_name='Дата'),
        ),
    ]
