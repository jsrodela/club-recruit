from django.shortcuts import render

from account.base import get_data


def index(request):
    data = get_data(request)
    return render(request, 'index/index.html', data)
