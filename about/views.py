from django.shortcuts import render

from account.base import get_data


def about(request):
    data = get_data(request)
    return render(request, 'about/about.html', data)
