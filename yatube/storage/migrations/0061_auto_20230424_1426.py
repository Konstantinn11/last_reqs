# Generated by Django 2.2.6 on 2023-04-24 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0060_auto_20230227_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='pack',
            field=models.TextField(blank=True, null=True, verbose_name='Место хранения упаковки'),
        ),
        migrations.AlterField(
            model_name='event',
            name='pub_day',
            field=models.TextField(default=datetime.date(2023, 4, 24), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2023, 4, 24), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2023, 4, 24), verbose_name='Дата'),
        ),
    ]
