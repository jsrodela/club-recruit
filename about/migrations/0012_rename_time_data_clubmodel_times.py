# Generated by Django 4.1.5 on 2024-02-07 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0011_remove_clubmodel_time_data_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clubmodel',
            old_name='time_data',
            new_name='times',
        ),
    ]