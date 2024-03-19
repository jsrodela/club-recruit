import json
import logging

from django.db import transaction
from django.shortcuts import render, redirect
from django.utils import timezone

from about.models import ClubModel
from account.base import get_data
from account.models import User
from .form_data import form_data
from .models import FormModel, TimeModel
from django.http import HttpResponse
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# 지원서 제출
def form(request, clubname):
    data = get_data(request)

    if 'user' not in data:
        data['error'] = "로그인 이후 신청하세요."
        return render(request, 'form/form.html', data)

    if FormModel.objects.filter(number=data['user'].id, club=clubname, archive=False):  # 유저 네임, 클럽네임을 가진 유저가 존재한다면
        data['error'] = "이미 지원서를 제출했습니다."
        return render(request, 'form/form.html', data)

    club_model = ClubModel.objects.get(code=clubname)
    now = timezone.localtime()
    if now < club_model.form_start or club_model.form_end < now:
        data['error'] = "지원서 제출 기간이 아닙니다."
        if request.POST:
            logger.warning(f"User {data['user'].id} tried to submit form to '{clubname}' after valid time; "
                           f"Form Data: {dict(request.POST)}")
        return render(request, 'form/form.html', data)

    if request.POST:
        submit = []
        user_id = data['user'].id

        submit_data = dict(request.POST)
        for key in submit_data:

            if key == 'csrfmiddlewaretoken':  # ignore csrf token
                continue

            answer = submit_data[key]  # ["answer"]
            if len(answer) == 1:
                answer = answer[0]  # "answer"

            submit.append({
                "question": key,
                "answer": answer
            })

        form_model = FormModel(number=user_id, club=ClubModel.objects.get(code=clubname), section=submit)
        form_model.save()
        logger.info(f"User {user_id} submitted form to '{clubname}': this is #{form_model.pk}")
        return redirect('/')

    data['clubname'] = clubname
    data['form_data'] = club_model.form_data
    # data['form_data'] = form_data
    return render(request, 'form/form.html', data)


# 지원서 확인 (지원자용)
def club(request, clubname):
    data = get_data(request)

    if 'user' not in data:
        data['error'] = "로그인 후 지원서 확인이 가능합니다."
        return render(request, 'form/form.html', data)

    user_id = data['user'].id

    try:
        form_submit = FormModel.objects.get(number=user_id, club=clubname, archive=False)
    except FormModel.DoesNotExist:
        data['error'] = "지원서를 찾을 수 없습니다."
        logger.error(f"User {user_id} failed to find its form to '{clubname}'")
        return render(request, 'form/form.html', data)

    if request.POST:

        # 지원 기간 확인
        club_model = ClubModel.objects.get(code=clubname)
        now = timezone.localtime()
        if now < club_model.form_start or club_model.form_end < now:
            data['error'] = "지원서 제출 기간이 끝나, 지원서를 삭제할 수 없습니다."
            return render(request, 'form/form.html', data)

        if 'delete_form' in request.POST:  # 지원 취소
            submit = FormModel.objects.get(number=user_id, club=clubname, archive=False)
            submit.archive = True
            submit.save()
            logger.info(f"User {user_id} archived its form #{submit.pk}, which is to '{clubname}'")
            return redirect('/')

    data['submit'] = json.dumps(form_submit.section)
    data['submit_user'] = User.objects.get(id=form_submit.number)
    data['delete_form'] = True

    club_model = ClubModel.objects.get(code=clubname)
    data['clubname'] = clubname
    data['form_data'] = club_model.form_data
    return render(request, 'form/form.html', data)


# 동아리 부장이 확인
def leader_view(request, form_id):
    data = get_data(request)

    if 'user' not in data:
        return redirect('/')

    user = data['user']

    if user.leader_of:
        leader_club = user.leader_of
    elif user.member_of:
        leader_club = user.member_of
    else:
        return redirect('/')

    try:
        form_submit = FormModel.objects.get(id=form_id, archive=False)
    except FormModel.DoesNotExist:
        data['error'] = '지원서를 찾을 수 없습니다.'
        logger.error(f"Leader/member {user.id} failed to find form #{form_id}")
        return render(request, 'form/form.html', data)

    if form_submit.club != leader_club:
        logger.warning(f"User {user.id} falsely tried to open form #{form_id}.")
        return redirect('/')

    data['submit_id'] = form_submit.id
    data['submit_user'] = User.objects.get(id=form_submit.number)
    data['submit'] = json.dumps(form_submit.section)
    data['leader_view'] = True

    data['clubname'] = leader_club.name
    data['form_data'] = leader_club.form_data
    # data['form_data'] = form_data

    return render(request, 'form/form.html', data)


# 면접 시간 선택: 요청 순차적으로 처리 (동기 방식)
@transaction.atomic
def time(request, clubname):
    data = get_data(request)

    if 'user' not in data:
        data['error'] = '로그인 후 면접 시간을 선택할 수 있습니다.'
        return render(request, 'form/time.html', data)

    user = data['user']

    try:
        apply = FormModel.objects.get(number=user.id, club=clubname, archive=False, first_result='P')
    except FormModel.DoesNotExist:
        data['error'] = '이 동아리에 합격하지 못했습니다.'
        logger.warning(f"From time selection page, cannot find PASSED form of {user.id} from '{clubname}'")
        return render(request, 'form/time.html', data)

    apply_club = apply.club

    if apply_club.time_start > timezone.localtime():
        data['error'] = '아직 면접시간 선택이 시작되지 않았어요.'
        return render(request, 'form/time.html', data)

    if apply.time_data:
        data['error'] = '이미 면접 시간을 선택했어요. 변경을 원하시면 면접시간 취소하기를 이용해 주세요'
        logger.warning(f'User {user.id} tried to RE-select time of form #{apply}')
        return render(request, 'form/time.html', data)

    if request.POST:
        time_id = request.POST.get('time_id')
        club_time = TimeModel.objects.select_for_update().get(club=apply_club, pk=time_id)
        # print(time_value)
        if club_time.current >= club_time.number:
            data['alert'] = '정원이 꽉 찼습니다. 다른 시간을 선택해주세요.'
            logger.info(
                f"User {user.id} tried to select time #{club_time.pk} which is full ({club_time.current}/{club_time.number})")
            return render(request, 'form/time.html', data)
        else:
            apply.time_data = (club_time.time_start + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
            club_time.form.set([apply])
            club_time.current += 1
            apply.save()
            club_time.save()

            logger.info(
                f"User {user.id} selected time #{club_time.pk} of form #{apply.pk}. The time data is '{apply.time_data}'")
            return redirect('/')

    time_data = TimeModel.objects.filter(club=apply_club).order_by('time_start')
    # prev_date = ''
    lst = []
    times = []
    first_date = True
    chkdate = ""
    for obj in time_data:  # KST 보정 적용
        if first_date:
            chkdate = (obj.time_start + timedelta(hours=9)).strftime('%m/%d')
            first_date = False
        if chkdate != (obj.time_start + timedelta(hours=9)).strftime('%m/%d'):
            lst.append({
                'date': chkdate,
                'times': times
            })
            chkdate = (obj.time_start + timedelta(hours=9)).strftime('%m/%d')
            times = []
        times.append({
            'start': (obj.time_start + timedelta(hours=9)).strftime('%H:%M'),
            'end': (obj.time_end + timedelta(hours=9)).strftime('%H:%M'),
            'number': obj.number,
            'current': obj.current,
            'id': obj.pk
        })
    lst.append({
        'date': chkdate,
        'times': times
    })

    data['time_data'] = lst
    data['club'] = apply_club
    return render(request, 'form/time.html', data)


def cancel(request, clubname):
    data = get_data(request)
    user_id = data['user'].id
    apply_club = ClubModel.objects.get(name=clubname)

    try:
        apply = FormModel.objects.get(number=user_id, club=apply_club, archive=False, first_result='P')
    except FormModel.DoesNotExist:
        logger.warning(f"From time cancel page, cannot find form of {user_id} from '{clubname}'")
        return redirect('/')

    if apply.time_data is None or not apply.time_data:  # 시간 데이터 없다면
        logger.warning(f"From time cancel page, no time selection at form #{apply.pk}")
        return redirect('/')

    try:
        apply_time = TimeModel.objects.get(form=apply, club=apply_club)
    except TimeModel.DoesNotExist:
        logger.warning(f"From time cancel page, cannot find TimeModel which is related to #{apply.pk}. "
                       f"The form has time_data of '{apply.time_data}'")
        return redirect('/')

    apply.time_data = None
    apply_time.form.set([None])
    apply_time.current -= 1
    apply.save()
    apply_time.save()

    logger.info(f"User {user_id} cancelled time #{apply_time.pk} of form #{apply.pk}")
    return redirect('/')


def select(request, clubname):
    data = get_data(request)
    user_id = data['user'].id

    if FormModel.objects.filter(number=user_id, second_result='S').exists():
        logger.warning(f"User {user_id} tried to re-select club {clubname}")
        return redirect('/')

    apply_club = ClubModel.objects.get(code=clubname)

    try:
        form = FormModel.objects.get(number=user_id, club=apply_club, first_result='P', second_result='P', archive=False)
    except FormModel.DoesNotExist:
        logger.warning(f"User {user_id} tried to select club {clubname}, which is not passed")
        return redirect('/')

    form.second_result = 'S'
    form.save()

    other_form = FormModel.objects.filter(number=user_id, first_result='P', second_result='P', archive=False)
    if other_form.exists():
        for give_up in other_form:
            give_up.second_result = 'G'
            for rank_up in FormModel.objects.filter(club=give_up.club, first_result = 'P', second_result = 'A', archive=False):
                if rank_up.additional_rank == 1:
                    rank_up.second_result = 'V'
                rank_up.additional_rank -= 1
                rank_up.save()
            give_up.save()

    form.save()

    answer = request.GET.get('signature')
    logger.info(f"User {user_id} selected club {apply_club.name}; signature: {answer}")
    return redirect(f'/?select={apply_club.name}')
