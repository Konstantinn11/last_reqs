# Generated by Django 2.2.6 on 2022-07-29 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0004_auto_20220729_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Number',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='номер конфигурации')),
            ],
            options={
                'verbose_name': 'Номер конфигурации',
                'verbose_name_plural': 'Нномера конфигурации',
                'ordering': ('number',),
            },
        ),
        migrations.AlterField(
            model_name='config',
            name='number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='numbers', to='configs.Number', verbose_name='Номер конфигурации'),
        ),
    ]
