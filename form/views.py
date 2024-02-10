import json

from django.shortcuts import render, redirect
from django.utils import timezone

from about.models import ClubModel
from account.base import get_data
from account.models import User
from .form_data import form_data
from .models import FormModel, TimeModel
from django.http import HttpResponse


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
        return render(request, 'form/form.html', data)

    if request.POST:
        submit = []
        user_id = data['user'].id

        print(request.POST)

        submit_data = dict(request.POST)

        for key in submit_data:

            print(key)

            if key == 'csrfmiddlewaretoken':  # ignore csrf token
                continue

            answer = submit_data[key]  # ["answer"]
            print('answer is ', answer)
            if len(answer) == 1:
                print(answer, 'is', answer[0])
                answer = answer[0]  # "answer"

            submit.append({
                "question": key,
                "answer": answer
            })

        print(submit)
        FormModel(number=user_id, club=ClubModel.objects.get(code=clubname), section=submit).save()
        return redirect('/')

    data['clubname'] = clubname
    data['form_data'] = club_model.form_data
    # data['form_data'] = form_data
    return render(request, 'form/form.html', data)


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
        return render(request, 'form/form.html', data)

    if form_submit.club != leader_club:
        return redirect('/')

    data['submit_id'] = form_submit.id
    data['submit_user'] = User.objects.get(id=form_submit.number)
    data['submit'] = json.dumps(form_submit.section)
    data['leader_view'] = True

    data['clubname'] = leader_club.name
    data['form_data'] = leader_club.form_data
    # data['form_data'] = form_data

    return render(request, 'form/form.html', data)


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
        return render(request, 'form/time.html', data)

    club = apply.club

    if club.time_start > timezone.localtime():
        data['error'] = '아직 면접시간 선택이 시작되지 않았어요.'
        return render(request, 'form/time.html', data)

    if apply.time:
        data['error'] = '이미 면접 시간을 선택했어요. 변경을 원하시면 하단의 문의하기를 눌러 문의해주세요. '
        return render(request, 'form/time.html', data)

    if request.POST:
        time_value = request.POST.get('time_value')
        time_date = time_value[0:2] + '-' + time_value[3:5]
        time_start = time_value[6:11]

        time_data = club.time_data
        # print(time_value)
        for i in range(len(time_data)):
            obj = time_data[i]
            # print(obj, time_date, time_start)

            if obj['date'].endswith(time_date) and obj['start'] == time_start:
                obj['current'] = int(obj['current'])
                obj['number'] = int(obj['number'])
                if obj['current'] >= obj['number']:
                    data['alert'] = '정원이 꽉 찼습니다. 다른 시간을 선택해주세요.'
                    continue
                else:
                    obj['current'] += 1
                    time_data[i] = obj
                    club.time_data = time_data
                    club.save()

                    # if apply.time:
                    #     prev_time = apply.time
                    #     prev_date = prev_time[0:2] + '-' + prev_time[3:5]
                    #     prev_start = prev_time[6:11]

                    apply.time = time_value
                    apply.save()
                    return redirect('/')

        data['alert'] = '오류가 발생했습니다. 오류가 지속되면 문의하기를 눌러 알려주세요.'

    time_data = sorted(club.time_data, key=lambda x: (x['date'], x['start'], x['end']))
    prev_date = ''
    lst = []
    times = []
    for obj in time_data:
        # print(obj)
        if obj['date'] != prev_date:
            if times:
                lst.append({
                    'date': prev_date[5:7] + "/" + prev_date[8:10],
                    'times': times
                })
            prev_date = obj['date']
            times = []
        times.append({
            'start': obj['start'],
            'end': obj['end'],
            'number': obj['number'],
            'current': obj['current'],
        })
    if times:
        lst.append({
            'date': prev_date[5:7] + "/" + prev_date[8:10],
            'times': times
        })

    data['time_data'] = lst
    data['club'] = club
    return render(request, 'form/time.html', data)


def cancel(request, clubname): # 미완성임, def time 기반
    data = get_data(request)

    if 'user' not in data:
        data['error'] = '로그인 후 면접 시간을 취소할 수 있습니다.'
        return render(request, 'form/time.html', data)

    user = data['user']

    try:
        apply = FormModel.objects.get(number=user.id, club=clubname, archive=False, first_result='P')
    except FormModel.DoesNotExist:
        data['error'] = '이 동아리에 합격하지 못했습니다.'
        return render(request, 'form/time.html', data)

    club = apply.club

    if club.time_start > timezone.localtime():
        data['error'] = '아직 면접시간 선택이 시작되지 않았어요.'
        return render(request, 'form/time.html', data)

    if request.POST:
        cancel_value = request.POST.get('cancel_value')
        cancel_date = cancel_value[0:2] + '-' + cancel_value[3:5]
        cancel_start = cancel_value[6:11]

        cancel_data = club.time_data
        # print(time_value)
        for i in range(len(cancel_data)):
            obj = cancel_data[i]
            # print(obj, time_date, time_start)

            if obj['date'].endswith(cancel_date) and obj['start'] == cancel_start:
                obj['current'] = int(obj['current'])
                obj['number'] = int(obj['number'])
                obj['current'] -= 1
                cancel_data[i] = obj
                club.time_data = cancel_data
                club.save()
                # if apply.time:
                #     prev_time = apply.time
                #     prev_date = prev_time[0:2] + '-' + prev_time[3:5]
                #     prev_start = prev_time[6:11]
                apply.time = cancel_value
                apply.save()
                return redirect('/')

        data['alert'] = '오류가 발생했습니다. 오류가 지속되면 문의하기를 눌러 알려주세요.'

    cancel_data = sorted(club.time_data, key=lambda x: (x['date'], x['start'], x['end']))
    prev_date = ''
    lst = []
    times = []
    for obj in cancel_data:
        # print(obj)
        if obj['date'] != prev_date:
            if times:
                lst.append({
                    'date': prev_date[5:7] + "/" + prev_date[8:10],
                    'times': times
                })
            prev_date = obj['date']
            times = []
        times.append({
            'start': obj['start'],
            'end': obj['end'],
            'number': obj['number'],
            'current': obj['current'],
        })
    if times:
        lst.append({
            'date': prev_date[5:7] + "/" + prev_date[8:10],
            'times': times
        })

    data['time_data'] = lst
    data['club'] = club
    return render(request, 'form/time.html', data)
