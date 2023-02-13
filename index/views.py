from django.shortcuts import render

from account.base import get_data
from form.models import FormModel


def index(request):
    data = get_data(request)

    if 'user' in data:
        array = FormModel.objects.filter(number=data['user'].id)

        club_names = []

    for i in array:
        club_names.append(i.club)  # club_names라는 리스트에 amas.club rodela.club 처럼 신청한 동아리.club만 추가


    data['club_names'] = club_names

    return render(request, 'index/index.html', data)
