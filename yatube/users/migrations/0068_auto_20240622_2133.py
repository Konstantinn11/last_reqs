# Generated by Django 2.2.6 on 2024-06-22 18:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0067_auto_20240531_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='phone_number',
            field=models.TextField(blank=True, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 6, 22, 21, 33, 5, 817615), null=True, verbose_name='Дата'),
        ),
    ]
