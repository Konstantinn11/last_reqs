# Generated by Django 2.2.6 on 2022-03-16 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0057_auto_20220315_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='day',
            field=models.DateTimeField(default=datetime.date(2022, 3, 16), verbose_name='Дата испытаний'),
        ),
    ]
