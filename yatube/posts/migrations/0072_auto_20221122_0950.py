# Generated by Django 2.2.6 on 2022-11-22 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0071_auto_20220804_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'ordering': ['state_id', '-created'], 'verbose_name': 'Обращение', 'verbose_name_plural': 'Обращения'},
        ),
    ]
