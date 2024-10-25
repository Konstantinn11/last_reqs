# Generated by Django 2.2.6 on 2022-11-30 12:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0018_auto_20221129_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 30, 12, 9, 8, 373904, tzinfo=utc), null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 30, 15, 9, 8, 373904), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='spec',
            field=models.TextField(blank=True, default='Д.А. Мыльников', null=True, verbose_name='Подписант'),
        ),
    ]
