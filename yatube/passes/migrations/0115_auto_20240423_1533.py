# Generated by Django 2.2.6 on 2024-04-23 12:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0114_auto_20240423_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 23, 15, 33, 20, 724628), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 23, 15, 33, 20, 723629), verbose_name='Дата'),
        ),
    ]
