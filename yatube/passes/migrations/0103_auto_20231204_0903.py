# Generated by Django 2.2.6 on 2023-12-04 06:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0102_auto_20231204_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 12, 4, 9, 3, 36, 587883), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 4, 9, 3, 36, 586883), verbose_name='Дата'),
        ),
    ]
