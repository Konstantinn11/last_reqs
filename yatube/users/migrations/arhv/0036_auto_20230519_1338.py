# Generated by Django 2.2.6 on 2023-05-19 10:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_auto_20230519_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 19, 13, 38, 36, 988602), null=True, verbose_name='Дата'),
        ),
    ]
