from django.db import models


# Create your models here.


class ImageModel(models.Model):
    club = models.CharField(max_length=10)
    image = models.FileField(null=True, upload_to="media/")


class ClubModel(models.Model):
    # 동아리 이름 (표시용 이름)
    name = models.CharField(max_length=100, default='테스트_동아리')

    # 동아리 코드 (영문 소문자, 10자 이내)
    code = models.CharField(max_length=10, default='test_club', unique=True)  # always english lowercase

    # 지원 시작 ~ 종료 시간
    form_start = models.DateTimeField(auto_now=True)
    form_end = models.DateTimeField(auto_now=True)

    # 메인페이지 배너 이미지와 설영
    index_banner_image = models.ForeignKey(ImageModel, related_name='index_banner_image+',
                                           on_delete=models.SET_NULL, null=True, blank=True)
    index_banner_description = models.TextField(default="동아리 소개 준비중")

    # 소개페이지 배경, 사진들, 소개글 (마크다운 문법)
    about_background = models.ForeignKey(ImageModel, related_name='about_background+',
                                         on_delete=models.SET_NULL, null=True, blank=True)
    about_images = models.ManyToManyField(ImageModel, related_name='about_images+', blank=True)
    about_text = models.TextField(default='# 동아리 소개 준비중\n동아리에서 아직 내용을 준비하는 중이에요.')

    # 동아리 로고 (왼쪽 메뉴)
    logo_image = models.ForeignKey(ImageModel, related_name='logo_image+',
                                   on_delete=models.SET_NULL, null=True, blank=True)
