# Generated by Django 2.2.6 on 2021-11-18 09:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0055_auto_20211021_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='day',
            field=models.DateTimeField(default=datetime.date(2021, 11, 18), verbose_name='Дата испытаний'),
        ),
    ]
