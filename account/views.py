from django.contrib import auth
from django.shortcuts import render, redirect
from .base import get_data


def login(request):
    data = get_data(request)
    if request.POST:
        form = request.POST

        _id = form.get('id')
        _pw = form.get('pw')
        user = auth.authenticate(id=_id, password=_pw)

        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            data['invalid'] = True
    return render(request, 'account/login.html', data)
