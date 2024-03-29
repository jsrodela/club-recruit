# Generated by Django 5.0.2 on 2024-03-03 10:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0009_formmodel_is_extra_timemodel_club_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timemodel',
            name='form',
        ),
        migrations.CreateModel(
            name='FormtoTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='form.formmodel')),
                ('time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='form.timemodel')),
            ],
        ),
        migrations.AddField(
            model_name='timemodel',
            name='form',
            field=models.ManyToManyField(blank=True, related_name='time_form+', through='form.FormtoTime', to='form.formmodel'),
        ),
    ]
