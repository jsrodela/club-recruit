import json

from django.db import models


# Create your models here.
class StatusModel(models.Model):
    STATUS = [('PREPARE', '동아리 홍보 기간'),
              ('FIRST_FORM', '1차 서류 지원'),
              ('FIRST_RESULT', '1차 서류합격 발표'),
              ('SECOND_INTERVIEW', '2차 면접 기간'),
              ('SECOND_RESULT', '최초합 발표'),
              ('ADD_FIRST_RESULT', '1차 추가합격 발표'),
              ('ADD_SECOND_RESULT', '2차 추가합격 발표'),
              ('ADD_THIRD_RESULT', '3차 추가합격 발표'),
              ('ADD_FORTH_RESULT', '4차 추가합격 발표'),
              ('ADDITIONAL', '추가모집 기간'),
              ('FINISH', '상설동아리 모집 종료')
              ]
    current = models.CharField(max_length=20, choices=STATUS, null=False, default='PREPARE')

    additional_rank = models.IntegerField(default=0)
