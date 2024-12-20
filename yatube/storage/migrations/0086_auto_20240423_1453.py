# Generated by Django 2.2.6 on 2024-04-23 11:53

import datetime
from django.db import migrations, models
import storage.models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0085_auto_20240115_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='pub_day',
            field=models.TextField(default=datetime.date(2024, 4, 23), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2024, 4, 23), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='image',
            field=models.ImageField(blank=True, help_text='Загрузите картинку', null=True, upload_to=storage.models.rename_file, verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2024, 4, 23), verbose_name='Дата'),
        ),
    ]
