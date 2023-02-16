from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .base import get_data

UserModel = auth.get_user_model()


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


def register(request):
    data = get_data(request)
    if request.POST:
        form = request.POST

        _id = form.get('id')
        _name = form.get('name')
        _phone = form.get('phone')
        _pw = form.get('pw')

        if UserModel.objects.filter(id=_id).exists():
            data['invalid'] = f"학번이 {_id}인 계정이 이미 존재합니다."
        else:
            try:
                validate_password(_pw)

                user = UserModel.objects.create_user(_id, _name, _phone, _pw)
                auth.login(request, user)
                return redirect('/')
            except ValidationError as err:
                data['invalid'] = err.messages[0]

    return render(request, 'account/register.html', data)


def logout(request):
    auth.logout(request)
    return redirect('/')
