# Generated by Django 2.2.6 on 2024-01-15 07:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0112_auto_20240115_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 1, 15, 10, 10, 39, 812412), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 15, 10, 10, 39, 812412), verbose_name='Дата'),
        ),
    ]
