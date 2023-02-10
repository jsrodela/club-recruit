import json

from django.db import models

# Create your models here.
class MyPageModel(models.Model):

    circle = models.JSONField(
        encoder=json.JSONEncoder,
        decoder=json.JSONDecoder
    )

    interview_time = models.JSONField(
        encoder=json.JSONEncoder,
        decoder=json.JSONDecoder
    )