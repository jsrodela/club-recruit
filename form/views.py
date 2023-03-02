import json

from django.shortcuts import render, redirect
from django.utils import timezone

from about.models import ClubModel
from account.base import get_data
from account.models import User
from .form_data import form_data
from .models import FormModel


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


def time(request):
    data = get_data(request)
    return render(request, 'form/time.html', data)
