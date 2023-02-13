from django.db import models


# Create your models here.

class ClubModel(models.Model):
    # 동아리 이름 (표시용 이름)
    name = models.CharField(max_length=100, default='테스트_동아리'),

    # 동아리 코드 (영문 소문자, 10자 이내)
    code = models.CharField(max_length=10, default='test_club'),  # always english lowercase

    # 동아리 소개 (마크다운 문법)
    about = models.TextField(default='# 동아리 소개 준비중\n동아리에서 아직 내용을 준비하는 중이에요.')

    # 지원 시작 ~ 종료 시간
    form_start = models.DateTimeField(auto_now=True)
    form_end = models.DateTimeField(auto_now=True)
