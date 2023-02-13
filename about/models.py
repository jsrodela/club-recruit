from django.db import models


# Create your models here.

class ClubModel(models.Model):
    name = models.CharField(max_length=100, default='테스트_동아리'),
    code = models.CharField(max_length=10, default='test_club'),  # always english lowercase
    about = models.TextField(default='# 동아리 소개 준비중\n동아리에서 아직 내용을 준비하는 중이에요.')
    form_start = models.DateTimeField(auto_now=True)
    form_end = models.DateTimeField(auto_now=True)
