import json

from django.db import models

# Create your models here.
from about.models import ClubModel


class FormModel(models.Model):
    number = models.IntegerField()

    club = models.ForeignKey(ClubModel, on_delete=models.PROTECT)

    # club = models.CharField(max_length=10)

    section = models.JSONField(
        encoder=json.JSONEncoder,
        decoder=json.JSONDecoder
    )

    submit_at = models.DateTimeField(auto_now_add=True)

    archive = models.BooleanField(default=False)
