# Generated by Django 2.2.6 on 2023-05-18 10:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_auto_20230517_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 18, 13, 57, 5, 99868), null=True, verbose_name='Дата'),
        ),
    ]
