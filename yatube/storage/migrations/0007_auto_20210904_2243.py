# Generated by Django 2.2.6 on 2021-09-04 19:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0006_auto_20210831_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='th',
            name='cz',
            field=models.FileField(blank=True, null=True, upload_to='storage/', verbose_name='Служебная записка'),
        ),
        migrations.AlterField(
            model_name='th',
            name='day',
            field=models.TextField(default=datetime.date(2021, 9, 4), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2021, 9, 4), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='th',
            field=models.FileField(blank=True, null=True, upload_to='storage/', verbose_name='Накладная'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2021, 9, 4), verbose_name='Дата'),
        ),
    ]
