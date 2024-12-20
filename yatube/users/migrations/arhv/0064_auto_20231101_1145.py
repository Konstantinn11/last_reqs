# Generated by Django 2.2.6 on 2023-11-01 08:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0063_auto_20231101_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='vaqs_access',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Доступ к отпускам'),
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 1, 11, 45, 28, 121812), null=True, verbose_name='Дата'),
        ),
    ]
