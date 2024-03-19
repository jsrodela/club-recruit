import json
import datetime

from django.db import models
from django.utils.timezone import now

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

    # 추가합격은 additional, 추가모집은 extra라 명명합시다.
    # A = 추가합격 대상자 (대기) / V = 추가합격 대상자 (표시) / S = 동아리 입부 선택 / G = 입부 포기
    RESULTS = [('W', 'WAIT'), ('P', 'PASS'), ('F', 'FAIL'),
               ('A', 'ADDITIONAL_PASS'), ('V', 'ADDITIONAL_PASS_VISIBLE'), ('S', 'SELECTED'), ('G', 'GIVE_UP')]
    first_result = models.CharField(max_length=1, choices=RESULTS, default='W')
    second_result = models.CharField(max_length=1, choices=RESULTS, default='W')

    additional_rank = models.IntegerField(null=False, default=0)

    # 추가모집 지원서일 경우 - 추가모집 결과는 FIRST_RESULT에 저장
    is_extra = models.BooleanField(default=False)
    # time = models.CharField(max_length=100, default='', blank=True)

    time_data = models.DateTimeField(null=True, blank=True)


'''
    동아리 부장이 TimeModel을 생성하여 시간을 지정하고,
    지원자가 시간을 선택하면 해당 지원자의 form이 연결되도록 합시다.
    (아니면 그냥 지원자 account를 연결해도 무방하구요)
    
    time_data에 json 형식으로 저장하는 방식 자체가 위험합니다!
    이 때문에 작년에 오류가 났던 것이구요.
    TimeModel에는 시간을 저장하고, 각각의 합격된 FormModel과 연결하여
    장고 모델로서 활용할 수 있도록 합시다.
    
    이렇게 구조가 변경되면 총 네 가지가 변경되어야 하겠네요.
    1. 지원자의 시간 선택 페이지: form/views.py time() (+ form/templates/time.html)
    2. 부장의 면접시간 지정 페이지: leader/views.py time_config() (+ leader/templates/time_config.html)
    3. 기존 부원들의 지원자 면접시간 확인 페이지: leader/views.py view_time() (+ leader/templates/view_time.html)
    4. 메인페이지 시간 확인 부분: index/views.py 
    
    화이팅입니다!!
'''


class TimeModel(models.Model):
    time_start = models.DateTimeField(default=now)  # 면접 시작시간
    time_end = models.DateTimeField(default=now)  # 면접 종료시간

    current = models.IntegerField(default=0)  # 현재 면접 예약 인원수
    number = models.IntegerField(default=10)  # 시간당 면접 정원

    form = models.ManyToManyField('FormModel', related_name='time_form+', through='FormtoTime',blank=True)
    club = models.ForeignKey(ClubModel, related_name='time_club+', on_delete=models.SET_NULL, null=True)

    # @TODO: 생각해보니 하나의 TimeModel에 여러 FormModel이 연결될 수 있음. ManyToMany로 바꿔야 할듯.
    # 그리고 FormModel에서 time_data 없애고, ManyToManyField의 related_name 속성 이용해서 연결하기.
    # 이왕 하는김에 다른 데이터들도 related_name으로 다 바꿔두면 좋은...데 시간이 없넹ㅎ

    # 2차 면접 시간 데이터
    # time_data = models.JSONField(encoder=json.JSONEncoder, decoder=json.JSONDecoder, default=list)

    # clubmodel 은 timemodel, timemodel 은 formmodel 참조

class FormtoTime(models.Model):
    form = models.ForeignKey(FormModel, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.ForeignKey(TimeModel, on_delete=models.SET_NULL, null=True, blank=True)