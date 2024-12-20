# Generated by Django 2.2.6 on 2021-08-27 12:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0037_auto_20210827_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.date(2021, 8, 27), help_text='формат ввода: YYYY-mm-dd', null=True, verbose_name='Дата испытаний'),
        ),
        migrations.AlterField(
            model_name='post',
            name='t_start',
            field=models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time', to='posts.Time', verbose_name='время начала'),
        ),
        migrations.AlterField(
            model_name='post',
            name='t_stop',
            field=models.ForeignKey(blank=True, default=21, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='times', to='posts.Time', verbose_name='время окончания'),
        ),
    ]
