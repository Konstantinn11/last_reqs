# Generated by Django 2.2.6 on 2024-12-03 14:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0071_auto_20241112_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 12, 3, 17, 12, 29, 978599), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='day_end',
            field=models.DateField(blank=True, null=True, verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='day_start',
            field=models.DateField(blank=True, null=True, verbose_name='Дата начала'),
        ),
    ]
