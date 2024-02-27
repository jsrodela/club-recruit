import logging
import random

from django.shortcuts import render

from about.models import ClubModel
from account.base import get_data
from form.models import FormModel
from index.models import StatusModel


logger = logging.getLogger(__name__)

def index(request):
    data = get_data(request)

    if 'user' in data:
        data['forms'] = FormModel.objects.filter(number=data['user'].id, archive=False)

    # if 'banner_club' in request.GET:  # /?banner_club=CODE
    #     data['banner_club'] = ClubModel.objects.get(code=request.GET.get('banner_club'))
    # elif ClubModel.objects.all().exists():  # 맨 처음에 동아리 없을 때 제외
    #     data['banner_club'] = random.choice(list(ClubModel.objects.all()))
    data['banner_clubs'] = ClubModel.objects.all()

    data['status'] = StatusModel.objects.get_or_create()[0]

    return render(request, 'index/index.html', data)


def club_relation(request):
    data = get_data(request)
    return render(request, 'index/clubRelation.html', data)
