import json

from django.db import models

# Create your models here.

class FormModel(models.Model):
    number = models.IntegerField()

    club = models.CharField(
        max_length=10
    )

    section = models.JSONField(
        encoder=json.JSONEncoder,
        decoder=json.JSONDecoder
    )