# Generated by Django 2.2.6 on 2021-06-17 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20210617_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='task_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='states', to='posts.Task_state', verbose_name='Статус'),
        ),
    ]
