# Generated by Django 2.2.6 on 2023-12-05 18:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0107_auto_20231205_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 12, 5, 21, 3, 51, 964995), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 5, 21, 3, 51, 963996), verbose_name='Дата'),
        ),
    ]
