# Generated by Django 4.1.5 on 2023-02-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("form", "0002_formmodel_submit_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="formmodel",
            name="archive",
            field=models.BooleanField(default=False),
        ),
    ]