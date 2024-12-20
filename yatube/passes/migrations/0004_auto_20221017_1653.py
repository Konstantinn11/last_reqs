# Generated by Django 2.2.6 on 2022-10-17 13:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0003_pass_pasport'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pass',
            options={'ordering': ('day', 'num'), 'verbose_name': 'Пропуск', 'verbose_name_plural': 'Пропуска'},
        ),
        migrations.AlterField(
            model_name='pass',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='day',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 17, 16, 53, 35, 280626), help_text='формат ввода: YYYY-mm-dd', null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='pass',
            name='num',
            field=models.TextField(unique=True, verbose_name='Номер'),
        ),
    ]
