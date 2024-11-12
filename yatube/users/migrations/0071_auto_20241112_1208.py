# Generated by Django 2.2.6 on 2024-11-12 09:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0070_auto_20240703_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 11, 12, 12, 8, 3, 589797), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='user_info',
            name='vacs_access',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Доступ к отпускам'),
        ),
    ]