import json

from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .base import get_data
from .models import User

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
            data['invalid'] = f"학번이 {_id}인 계정이 이미 존재합니다. <a href='https://github.com/RoDeLa6/club-recruit/blob/main/account/docs/contact.md' target='_blank' style='color: var(--main-color);'>[문의하기]</a>"
        else:
            try:
                validate_password(_pw)

                user = UserModel.objects.create_user(_id, _name, _phone, _pw)
                auth.login(request, user)
                return redirect('/')
            except ValidationError as err:
                data['invalid'] = err.messages[0]

    # 체크박스 동의 여부 확인
    consent_given = form.get('consent') == 'on'
    if not consent_given:
        data['invalid'] = "개인정보 수집 및 이용에 동의해야 회원가입이 가능합니다."
        return render(request, 'account/register.html', data)



def logout(request):
    auth.logout(request)
    return redirect('/')


@csrf_exempt
def api(request):
    if request.method == "POST":
        body = json.loads(request.body)
        _id = body.get('id')
        _pw = body.get('pw')
        user = auth.authenticate(id=_id, password=_pw)
        if user:
            return HttpResponse(json.dumps({
                'number': user.id,
            }))
        else:
            return HttpResponse(json.dumps({
                'error': 'cannot find user',
            }))

    return redirect('/')


def password(request):
    data = get_data(request)
    user = data['user']
    if not user.is_superuser:
        return redirect('/')

    if request.POST:
        _id = request.POST.get('id')
        _pw = request.POST.get('pw')

        try:
            validate_password(_pw)
            target = User.objects.get(id=_id)
            target.set_password(_pw)
            target.save()
            data['message'] = '비밀번호를 성공적으로 변경하였습니다.'
        except ValidationError as err:
            data['message'] = err.messages[0]
        except Exception as ex:
            data['message'] = str(ex)

    return render(request, 'account/password.html', data)
