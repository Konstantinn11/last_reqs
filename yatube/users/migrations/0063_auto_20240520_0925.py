# Generated by Django 2.2.6 on 2024-05-20 06:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0062_auto_20240520_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_widgets',
            name='widgets_order',
            field=models.TextField(blank=True, null=True, verbose_name='Порядок виджетов'),
        ),
        migrations.AlterField(
            model_name='log',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 20, 9, 25, 47, 818721), null=True, verbose_name='Дата'),
        ),
        migrations.DeleteModel(
            name='User_widgets_order',
        ),
    ]
