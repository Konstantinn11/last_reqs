# Generated by Django 2.2.6 on 2023-05-27 18:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_auto_20230519_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 27, 21, 7, 21, 540008), null=True, verbose_name='Дата'),
        ),
    ]
