# Generated by Django 2.2.6 on 2022-04-04 10:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0060_auto_20220318_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='t_start_html',
            field=models.TextField(blank=True, null=True, verbose_name='время начала_html'),
        ),
        migrations.AddField(
            model_name='post',
            name='t_stop_html',
            field=models.TextField(blank=True, null=True, verbose_name='время завершения_html'),
        ),
        migrations.AlterField(
            model_name='post',
            name='day',
            field=models.DateTimeField(default=datetime.date(2022, 4, 4), verbose_name='Дата испытаний'),
        ),
        migrations.AlterField(
            model_name='post',
            name='t_start',
            field=models.ForeignKey(default=17, help_text='время начала испытаний должно быть строго меньше времени завершения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time', to='posts.Time', verbose_name='время начала'),
        ),
        migrations.AlterField(
            model_name='post',
            name='t_stop',
            field=models.ForeignKey(default=27, help_text='время завершения испытаний должно быть строго больше времени начала', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='times', to='posts.Time', verbose_name='время окончания'),
        ),
    ]
