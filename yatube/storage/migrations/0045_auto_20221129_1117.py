# Generated by Django 2.2.6 on 2022-11-29 08:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0044_auto_20221127_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 11, 29), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 11, 29), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2022, 11, 29), verbose_name='Дата'),
        ),
    ]
