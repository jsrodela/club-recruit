# Generated by Django 4.1.5 on 2023-02-14 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("about", "0011_alter_clubmodel_form_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="clubmodel",
            name="form_edit_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
