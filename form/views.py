import json

from django.shortcuts import render, redirect

from about.models import ClubModel
from account.base import get_data
from .form_data import form_data
from .models import FormModel


def form(request, clubname):
    data = get_data(request)

    if 'user' not in data:
        data['error'] = "로그인 이후 신청하세요."
        return render(request, 'form/form.html', data)

    elif FormModel.objects.filter(number=data['user'].id, club=clubname, archive=False):  # 유저 네임, 클럽네임을 가진 유저가 존재한다면
        data['error'] = "이미 지원서를 제출했습니다."
        return render(request, 'form/form.html', data)

    else:
        pass

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

    club_model = ClubModel.objects.get(code=clubname)
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
        if 'delete_form' in request.POST:  # 지원 취소
            submit = FormModel.objects.get(number=user_id, club=clubname, archive=False)
            submit.archive = True
            submit.save()
            return redirect('/')

    data['submit'] = json.dumps(form_submit.section)

    club_model = ClubModel.objects.get(code=clubname)
    data['clubname'] = clubname
    data['form_data'] = club_model.form_data
    return render(request, 'form/form.html', data)
