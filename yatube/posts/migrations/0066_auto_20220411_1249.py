# Generated by Django 2.2.6 on 2022-04-11 09:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0065_auto_20220408_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='day',
            field=models.DateTimeField(default=datetime.date(2022, 4, 11), verbose_name='Дата испытаний'),
        ),
    ]
