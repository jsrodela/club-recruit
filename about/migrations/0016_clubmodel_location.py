# Generated by Django 5.0.3 on 2024-03-11 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0015_remove_clubmodel_times_clubmodel_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubmodel',
            name='location',
            field=models.CharField(default='추후 안내 예정', max_length=100),
        ),
    ]
