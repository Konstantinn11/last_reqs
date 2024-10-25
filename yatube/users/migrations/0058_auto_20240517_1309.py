# Generated by Django 2.2.6 on 2024-05-17 10:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0057_auto_20240514_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_widgets',
            name='calc',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Калькулятор'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='mess',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Мессенджер'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='news',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Новости'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='notes',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Заметки'),
        ),
        migrations.AddField(
            model_name='user_widgets',
            name='users',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Сотрудники'),
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 17, 13, 9, 32, 769321), null=True, verbose_name='Дата'),
        ),
    ]
