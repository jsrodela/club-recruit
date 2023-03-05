from datetime import datetime

import pytz
from django.shortcuts import render, redirect

# Create your views here.
from about.models import ImageModel
from account.base import get_data
from account.models import User
from form import form_data
from form.models import FormModel


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
            club.form_start = datetime.fromisoformat(submit.get('form_start') + ":00+09:00")
            club.form_end = datetime.fromisoformat(submit.get('form_end') + ":00+09:00")
        if 'member_add' in submit:
            member_id = submit.get('member_add')
            try:
                member = User.objects.get(id=member_id)
                if member.member_of:  # if already member in another club
                    data['error'] = f'{member_id} 학생은 이미 다른 동아리의 부원입니다.'
                else:
                    member.member_of = club
                    member.save()
                    club.members.append(member_id)
            except User.DoesNotExist:
                data['error'] = f'{member_id} 계정을 찾을 수 없어요.'

        if 'member_remove' in submit:
            member_id = submit.get('member_remove')
            if member_id in club.members:
                try:
                    member = User.objects.get(id=member_id)
                    if member.member_of.code != club.code:
                        data['error'] = f'{member_id} 학생은 이 동아리의 부원이 아니에요. 데이터가 꼬인 것 같은데, 로델라 부장에게 전해주세요.'
                    else:
                        member.member_of = None
                        member.save()
                        club.members.remove(member_id)
                except User.DoesNotExist:
                    data['error'] = f'{member_id} 계정을 찾을 수 없어요.'
            else:
                data['error'] = f'{member_id} 학생은 이 동아리의 부원이 아니에요.'

        club.save()

    data['club_form_start'] = club.form_start.astimezone(pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%dT%H:%M")
    data['club_form_end'] = club.form_end.astimezone(pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%dT%H:%M")

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
        form_user = User.objects.get(id=form.number)
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


def time_config(request):
    data = get_data(request)

    if 'user' not in data or data['user'].leader_of is None:
        return redirect('/')

    user = data['user']
    club = user.leader_of

    data['club'] = club
    return render(request, "leader/time_config.html", data)
