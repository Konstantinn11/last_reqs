# Generated by Django 2.2.6 on 2023-08-17 06:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0046_auto_20230808_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 17, 9, 4, 34, 871285), null=True, verbose_name='Дата'),
        ),
    ]
