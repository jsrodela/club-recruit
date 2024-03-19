import json
import logging
from datetime import datetime

from django.http import HttpResponse
from django.utils.timezone import make_aware

import pytz
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from about.models import ImageModel
from account.base import get_data
from account.models import User
from form import form_data
from form.models import FormModel
from about.models import ClubModel
from form.models import TimeModel



logger = logging.getLogger(__name__)


def club_config(request):
    data = get_data(request)
    if 'user' not in data or data['user'].leader_of is None:
        return redirect('/')

    user = data['user']
    club = user.leader_of

    data['club'] = club

    if request.POST:
        submit = request.POST
        file = request.FILES

        if 'club_name' in submit:
            club.name = submit.get('club_name')
        if 'logo_image' in file:
            club.logo_image = new_image('logo_image', club, file, user)
        if 'index_banner_description' in submit:
            club.index_banner_description = submit.get('index_banner_description')
        if 'index_banner_image' in file:
            club.index_banner_image = new_image('index_banner_image', club, file, user)
        if 'index_banner_color' in submit:
            club.index_banner_color = submit.get('index_banner_color')
        if 'about_background' in file:
            club.about_background = new_image('about_background', club, file, user)
        if 'about_image_add' in file:
            club.about_images.add(new_image('about_image_add', club, file, user))
        if 'about_image_remove' in submit:
            for target_id in submit.getlist('about_image_remove'):
                target = ImageModel.objects.get(id=target_id)
                club.about_images.remove(target)
        if 'about_text' in submit:
            club.about_text = submit.get('about_text')
        if 'form_change' in submit:
            if submit.get('kakao_url'):
                club.form_data = {'items': []}
                club.kakao_url = submit.get('kakao_url')
            else:
                # ExtForm과 연동하여 reload하고 getitem 하기
                club.form_data = form_data.reload_form(club.code)
                club.kakao_url = ""
        if 'form_start' in submit:
            club.form_start = make_aware(datetime.fromisoformat(submit.get('form_start')))
            club.form_end = make_aware(datetime.fromisoformat(submit.get('form_end')))

        if 'add_location' in submit:
            club.location = submit.get('location')

        if 'member_add' in submit:
            member_id = submit.get('member_add')
            try:
                member = User.objects.get(id=member_id)
                if member.member_of:  # if already member in another club
                    data['error'] = f'{member_id} 학생은 이미 다른 동아리의 부원입니다.'
                else:
                    member.member_of = club
                    member.save()
            except User.DoesNotExist:
                data['error'] = f'{member_id} 계정을 찾을 수 없어요.'

        if 'member_remove' in submit:
            member_id = submit.get('member_remove')
            try:
                member = User.objects.get(id=member_id)
                if member.member_of is None or member.member_of != club:
                    data['error'] = f'{member_id} 학생은 이 동아리의 부원이 아니에요.'
                else:
                    member.member_of = None
                    member.save()
            except User.DoesNotExist:
                data['error'] = f'{member_id} 계정을 찾을 수 없어요.'

        club.save()

    data['club_members'] = User.objects.filter(member_of=club)

    return render(request, 'leader/club_config.html', data)


def new_image(name, club, file, user):
    image = file.get(name)
    image_model = ImageModel(club=club.code, image=image, uploaded_by=user.id)
    image_model.save()
    return image_model


def view_forms(request):
    data = get_data(request)

    if 'user' not in data:
        return redirect('/')

    user = data['user']
    if data['user'].leader_of:
        club = user.leader_of
        data['is_leader'] = True
    elif data['user'].member_of:
        club = user.member_of
    else:
        return redirect('/')

    data['club'] = club

    if 'show_archive' in request.GET:
        forms = FormModel.objects.filter(club=club.code)
        data['show_archive'] = True
    else:
        forms = FormModel.objects.filter(club=club.code, archive=False)
        data['show_archive'] = False

    lst = []
    for form in forms:
        try:
            form_user = User.objects.get(id=form.number)
        except FormModel.DoesNotExist:
            data['error'] = "데이터에 문제가 발생했어요. 로델라 부장에게 이 오류를 보고해 주세요"
            return render(request, 'leader/view_forms.html', data)
        lst.append({
            'id': form.id,
            'number': form.number,
            'name': form_user.name,
            "phone": form_user.phone,
            'submit_at': form.submit_at,
            'archive': form.archive
        })
    data['forms'] = lst

    return render(request, 'leader/view_forms.html', data)


def time_config(request):  # timemodel 대응 수정 완료
    data = get_data(request)

    if 'user' not in data or data['user'].leader_of is None:
        return redirect('/')

    user = data['user']
    club = ClubModel.objects.get(code=user.leader_of.code)

    if request.POST:
        # print(club.code)
        # print(request.POST)
        post_data = request.POST
        club.time_use = True
        club.time_start = make_aware(datetime.fromisoformat(post_data.get('time_activate')))  # 면접 시간 선택 오픈

        for time in json.loads(post_data.get('time_data')):
            time_model = TimeModel()
            time_model.time_start = time['date'] + " " + time['start'] + "+09:00"
            time_model.time_end = time['date'] + " " + time['end'] + "+09:00"
            time_model.number = time['number']
            time_model.club = club
            print(time_model.time_start)
            time_model.save()

        club.save()

    data['club'] = club
    time_exists = TimeModel.objects.filter(club=club)
    data['time_exists'] = time_exists
    # data['time_start'] = club.times.all().time_start.astimezone(pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%dT%H:%M")
    return render(request, "leader/time_config.html", data)


def first_result(request):
    data = get_data(request)

    if 'user' not in data or data['user'].leader_of is None:
        return redirect('/')

    user = data['user']
    club = user.leader_of

    if request.POST:
        print(request.POST)
        for key in dict(request.POST):
            if key == 'csrfmiddlewaretoken':
                continue

            target = FormModel.objects.get(id=key)
            target.first_result = 'P'
            target.save()

        fails = FormModel.objects.filter(club=club.code, archive=False, first_result='W')
        for fail in fails:
            fail.first_result = 'F'
            fail.save()

    passes = FormModel.objects.filter(club=club.code, archive=False, first_result='P')
    if passes.exists():
        lst = []
        all_phone, pass_phone, fail_phone = [], [], []

        for form in FormModel.objects.filter(club=club.code, archive=False).order_by('number'):
            form_user = User.objects.get(id=form.number)
            phone = form_user.phone.as_national
            all_phone.append(phone)
            if form.first_result == 'P':
                lst.append({
                    'id': form.id,
                    'number': form.number,
                    'name': form_user.name,
                    'phone': form_user.phone,
                })
                pass_phone.append(phone)
            elif form.first_result == 'F':
                fail_phone.append(phone)

        data['all_phone'] = ",".join(all_phone)
        data['pass_phone'] = ", ".join(pass_phone)
        data['fail_phone'] = ", ".join(fail_phone)

    else:
        data['not_done'] = True
        forms = FormModel.objects.filter(club=club.code, archive=False)

        lst = []
        for form in forms:
            form_user = User.objects.get(id=form.number)
            lst.append({
                'id': form.id,
                'number': form.number,
                'name': form_user.name,
            })
    data['forms'] = lst

    data['club'] = club
    return render(request, "leader/first_result.html", data)


def every_forms(request):
    data = get_data(request)

    if 'user' not in data or data['user'].leader_of is None:
        return redirect('/')

    user = data['user']
    club = user.leader_of

    forms = FormModel.objects.filter(club=club.code, archive=False)
    lst = []
    for form in forms:
        form_user = User.objects.get(id=form.number)
        submit = form.section
        print(submit)
        lines = [f'{form_user.id} {form_user.name} (#{form.id}) {form_user.phone}']
        for obj in submit:
            if obj['answer'] == '--etc--':
                continue
            elif '--etc--' in obj['answer']:
                obj['answer'].remove('--etc--')
            lines.append(str(obj['answer']))
        lst.append(" /\n".join(lines))

    data['submits'] = "\n\n-----\n\n".join(lst)
    data['club'] = club
    return render(request, "leader/every_forms.html", data)


def view_time(request):  # timemodel 대응 수정 완료

    data = get_data(request)

    if 'user' not in data:
        return redirect('/')

    user = data['user']
    if data['user'].leader_of:
        club = user.leader_of
        # data['is_leader'] = True
    elif data['user'].member_of:
        club = user.member_of
    else:
        return redirect('/')

    data['club'] = club

    forms = FormModel.objects.filter(club=club, archive=False, first_result='P').order_by('time_data', 'number')

    lst = []
    lst_blank = []
    for form in forms:
        target_user = User.objects.get(id=form.number)
        obj = {
            'time': form.time_data,
            'number': target_user.id,
            'name': target_user.name,
            'id': form.id,
            'phone': target_user.phone
        }

        if form.time_data:
            lst.append(obj)
        else:  # blank
            lst_blank.append(obj)

    lst.extend(lst_blank)
    data['forms'] = lst
    return render(request, 'leader/view_time.html', data)


def second_result(request):
    data = get_data(request)
    if 'user' not in data or data['user'].leader_of is None:
        return redirect('/')

    club = data['user'].leader_of

    # 이미 2차 합격자를 선택한 경우 보기 페이지로
    if FormModel.objects.filter(club=club, first_result='P', second_result='P', archive=False).exists():
        return redirect('/leader/view_selection')

    if FormModel.objects.filter(club=club, first_result='P', second_result='S', archive=False).exists():
        return redirect('/leader/view_selection')

    if FormModel.objects.filter(club=club, first_result='P', second_result='G', archive=False).exists():
        return redirect('/leader/view_selection')

    if request.POST:
        result_data = request.POST.get('result_data')
        result_data = json.loads(result_data)
        for pass_user in result_data[0] + result_data[1]:
            user_id = pass_user['user_id']
            form = FormModel.objects.get(number=user_id, club=club, first_result='P', archive=False)
            form.second_result = 'P'
            form.save()

        # @TODO: 추가합격 form 처리, 동아리별 최대 추합 인원 저장, 미선택 인원 탈락 처리

        '''for additonal_pass_user in result_data[2] + result_data[3]: 
            user_id = additonal_pass_user['user_id']
            rank = additonal_pass_user['rank']
            form = FormModel.objects.get(number=user_id, club=club, first_result='P', archive=False)
            form.second_result = 'A'
            form.additional_rank = rank
            form.save()'''

        try:
            others = FormModel.objects.filter(club=club, first_result='P', second_result='W', archive=False)
            for fail_form in others:
                fail_form.second_result = 'F'
                fail_form.save()
        except FormModel.DoesNotExist:
            pass

        logger.info(f"Leader {data['user'].id} issued second_result: {result_data}")

        return redirect('/')

    data['club'] = club
    return render(request, 'leader/second_result.html', data)


# second_result에서 사용됨
@csrf_exempt
def second_result_check_user(request):
    data = get_data(request)

    if 'user' not in data or data['user'].leader_of is None:
        return redirect('/')

    club = data['user'].leader_of

    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body['user_id']
        user_name = body['user_name']
        try:
            user = User.objects.get(id=user_id, name=user_name)
            form = FormModel.objects.get(number=user.id, club=club, archive=False)

            if form.first_result != 'P':
                return HttpResponse(json.dumps({
                    'error': f'\'{user_id} {user_name}\' 학생은 1차 서류지원 합격자가 아닙니다.'
                }))

            if form.second_result != 'W' and form.second_result != 'F':
                return HttpResponse(json.dumps({
                    'error': f'\'{user_id} {user_name}\' 이미 합격/불합격자로 등록된 학생입니다.'
                }))

            # TimeModel 체크? (면접 봤는지) - 면접 따로 잡아서 봤을수도...

            return HttpResponse(json.dumps({
                'user_id': user.id,
                'user_name': user.name,
                'form_id': form.id
            }))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({
                'error': f'\'{user_id} {user_name}\' 학생을 찾을 수 없습니다.'
            }))
        except FormModel.DoesNotExist:
            return HttpResponse(json.dumps({
                'error': f'\'{user_id} {user_name}\' 학생은 이 동아리에 지원하지 않았습니다.'
            }))

    return redirect('/')


# @TODO: Add log

def view_selection(request):  # view_time 기반
    data = get_data(request)

    if 'user' not in data:
        return redirect('/')

    user = data['user']
    if data['user'].leader_of:
        club = user.leader_of
        # data['is_leader'] = True
    elif data['user'].member_of:
        club = user.member_of
    else:
        return redirect('/')

    data['club'] = club

    forms = FormModel.objects.filter(club=club, archive=False, first_result='P').order_by('number')
    lst = []
    for form in forms:
        if form.second_result == 'F' or form.second_result == 'W':
            continue
        target_user = User.objects.get(id=form.number)
        obj = {
            'selection': form.second_result,
            'number': target_user.id,
            'name': target_user.name,
            'id': form.id,
            'phone': target_user.phone
        }
        lst.append(obj)
    data['forms'] = lst
    return render(request, 'leader/view_selection.html', data)
