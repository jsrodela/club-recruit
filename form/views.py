from django.shortcuts import render

from account.base import get_data


def form(request):
    data = get_data(request)
    return render(request, 'form/form.html', data)
