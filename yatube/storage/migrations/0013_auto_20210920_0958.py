# Generated by Django 2.2.6 on 2021-09-20 06:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0012_auto_20210909_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='box',
            field=models.TextField(blank=True, null=True, verbose_name='Номер коробки'),
        ),
        migrations.AddField(
            model_name='unit',
            name='number',
            field=models.TextField(blank=True, null=True, verbose_name='Номер учетный'),
        ),
        migrations.AddField(
            model_name='unit',
            name='stend',
            field=models.TextField(blank=True, null=True, verbose_name='Стенд'),
        ),
        migrations.AlterField(
            model_name='th',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.date(2021, 9, 20), help_text='формат ввода: YYYY-mm-dd', null=True, verbose_name='Дата испытаний'),
        ),
        migrations.AlterField(
            model_name='th',
            name='pub_day',
            field=models.TextField(default=datetime.date(2021, 9, 20), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='pub_day',
            field=models.TextField(default=datetime.date(2021, 9, 20), verbose_name='Дата'),
        ),
    ]
