# Generated by Django 2.2.6 on 2024-01-15 07:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0077_auto_20231205_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='day',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата испытаний'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='post',
            name='reason',
            field=models.TextField(default=1, verbose_name='Основания для проведения испытаний'),
            preserve_default=False,
        ),
    ]
