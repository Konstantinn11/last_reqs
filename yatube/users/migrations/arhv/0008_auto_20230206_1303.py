# Generated by Django 2.2.6 on 2023-02-06 10:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20230205_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 6, 13, 3, 57, 732998), null=True, verbose_name='Дата'),
        ),
    ]
