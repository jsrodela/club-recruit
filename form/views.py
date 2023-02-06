from django.shortcuts import render

from account.base import get_data
from .form_data import form_data


def form(request):
    data = get_data(request)
    data['form_data'] = form_data
    return render(request, 'form/form.html', data)
