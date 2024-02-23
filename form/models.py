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

    RESULTS = [('W', 'WAIT'), ('P', 'PASS'), ('F', 'FAIL'), ('A', 'ADDITION_PASS')]

    first_result = models.CharField(max_length=1, choices=RESULTS, default='W')
    second_result = models.CharField(max_length=1, choices=RESULTS, default='W')
    additional_result = models.CharField(max_length=1, choices=RESULTS, default='W')
    # time = models.CharField(max_length=100, default='', blank=True)

    global time_data
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
    time_data_list = json.loads(time_data)
    for time_data in time_data_list:
        time_start = datetime.strptime(f"{time_data['date']} {time_data['start']}", "%Y-%m-%d %H:%M")
        time_end = datetime.strptime(f"{time_data['date']} {time_data['end']}", "%Y-%m-%d %H:%M")
        number = time_data["number"]
        current = time_data["current"]
        # TimeModel 인스턴스 생성




    form = models.ForeignKey(FormModel, related_name='time_form+', on_delete=models.SET_NULL, null=True, blank=True)


    # 2차 면접 시간 데이터
    # time_data = models.JSONField(encoder=json.JSONEncoder, decoder=json.JSONDecoder, default=list)

    # clubmodel 은 timemodel, timemodel 은 formmodel 참조
