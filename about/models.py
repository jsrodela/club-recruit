import json
from datetime import datetime

from django.db import models


# Create your models here.


def form_data_default():
    return {
        "title": "지원서 정보 없음",
        "description": "아직 동아리에서 지원서 양식을 제공하지 않았습니다.",
        "items": []
    }


class ImageModel(models.Model):
    club = models.CharField(max_length=10)
    image = models.FileField(null=True, upload_to="")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.IntegerField()


class ClubModel(models.Model):
    # 동아리 이름 (표시용 이름)
    name = models.CharField(max_length=100, default='테스트_동아리')

    # 동아리 코드 (영문 소문자, 10자 이내)
    code = models.CharField(max_length=10, default='test_club', unique=True, primary_key=True)  # always english lowercase

    # 지원 시작 ~ 종료 시간
    form_start = models.DateTimeField(default=datetime.now)
    form_end = models.DateTimeField(default=datetime.now)

    # 메인페이지 배너 이미지와 설영, 이름 색깔
    index_banner_image = models.ForeignKey(ImageModel, related_name='index_banner_image+',
                                           on_delete=models.SET_NULL, null=True, blank=True)
    index_banner_description = models.TextField(default="동아리 소개 준비중")
    index_banner_color = models.CharField(max_length=7, default="#000000")

    # 소개페이지 배경, 사진들, 소개글 (마크다운 문법)
    about_background = models.ForeignKey(ImageModel, related_name='about_background+',
                                         on_delete=models.SET_NULL, null=True, blank=True)
    about_images = models.ManyToManyField(ImageModel, related_name='about_images+', blank=True)
    about_text = models.TextField(default='# 동아리 소개 준비중\n동아리에서 아직 내용을 준비하는 중이에요.')

    # 동아리 로고 (왼쪽 메뉴)
    logo_image = models.ForeignKey(ImageModel, related_name='logo_image+',
                                   on_delete=models.SET_NULL, null=True, blank=True)

    # 설문지 양식 (구글폼과 동기화하려면 leader 페이지에서 적용)
    form_data = models.JSONField(encoder=json.JSONEncoder, decoder=json.JSONDecoder, default=form_data_default)

    # 설문지 수정 링크
    form_edit_url = models.URLField(null=True, blank=True)

    # 설문지 미사용 시 카카오톡 링크
    kakao_url = models.URLField(null=True, blank=True, default="")

    # 멤버 목록 (지원서 및 면접시간 확인 가능)
    members = models.JSONField(encoder=json.JSONEncoder, decoder=json.JSONDecoder, default=list)

    # 2차 면접 시간 선택 사용 여부
    time_use = models.BooleanField(default=False)

    # 2차 면접 시간 데이터
    time_data = models.JSONField(encoder=json.JSONEncoder, decoder=json.JSONDecoder, default=list)
