# Generated by Django 4.1.5 on 2023-03-02 16:55

from django.db import migrations, models
import json.decoder
import json.encoder


class Migration(migrations.Migration):

    dependencies = [
        ("about", "0005_clubmodel_index_banner_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="clubmodel",
            name="members",
            field=models.JSONField(
                decoder=json.decoder.JSONDecoder,
                default=list,
                encoder=json.encoder.JSONEncoder,
            ),
        ),
    ]
