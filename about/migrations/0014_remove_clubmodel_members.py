# Generated by Django 4.1.5 on 2024-02-22 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0013_alter_clubmodel_form_end_alter_clubmodel_form_start_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubmodel',
            name='members',
        ),
    ]
