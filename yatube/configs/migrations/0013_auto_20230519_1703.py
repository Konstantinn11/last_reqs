# Generated by Django 2.2.6 on 2023-05-19 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0012_changes_confirm'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='changes',
            options={'ordering': ('number', 'unit', '-id'), 'verbose_name': 'Запись о изменении', 'verbose_name_plural': 'Записи о изменениях'},
        ),
        migrations.AlterModelOptions(
            name='changes_confirm',
            options={'ordering': ('number', 'unit', '-id'), 'verbose_name': 'Подтвержденная запись о изменении', 'verbose_name_plural': 'Подтвержденные записи о изменениях'},
        ),
    ]
