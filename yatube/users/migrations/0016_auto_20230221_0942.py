# Generated by Django 2.2.6 on 2023-02-21 06:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20230221_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 21, 9, 42, 33, 900013), null=True, verbose_name='Дата'),
        ),
    ]
