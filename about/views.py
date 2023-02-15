from datetime import datetime

from django.shortcuts import render, redirect
from django.utils import timezone

from about.models import ClubModel, ImageModel
from account.base import get_data
from form import form_data


def about(request, clubname):
    data = get_data(request)
    club = ClubModel.objects.get(code=clubname)
    if club is None:
        return redirect('/')
    data['club'] = club
    return render(request, 'about/about.html', data)


def leader(request):
    data = get_data(request)
    if 'user' not in data or data['user'].leader_of is None:
        return redirect('/')

    club = data['user'].leader_of
    data['club'] = club

    if request.POST:
        submit = request.POST
        file = request.FILES

        if 'club_name' in submit:
            club.name = submit.get('club_name')
        if 'index_banner_description' in submit:
            club.index_banner_description = submit.get('index_banner_description')
        if 'index_banner_image' in file:
            club.index_banner_image = new_image('index_banner_image', club, file)
        if 'about_background' in file:
            club.about_background = new_image('about_background', club, file)
        if 'about_image_add' in file:
            club.about_images.add(new_image('about_image_add', club, file))
        if 'about_image_remove' in submit:
            for target_id in submit.getlist('about_image_remove'):
                target = ImageModel.objects.get(id=target_id)
                club.about_images.remove(target)
        if 'about_text' in submit:
            club.about_text = submit.get('about_text')
        if 'form_change' in submit:
            # ExtForm과 연동하여 reload하고 getitem 하기
            club.form_data = form_data.reload_form(club.code)
            pass
        if 'form_start' in submit:
            club.form_start = datetime.fromisoformat(submit.get('form_start')+"+09:00")
            club.form_end = datetime.fromisoformat(submit.get('form_end')+"+09:00")

        club.save()

    data['club_form_start'] = club.form_start.strftime("%Y-%m-%dT%H:%M:%S")
    data['club_form_end'] = club.form_end.strftime("%Y-%m-%dT%H:%M:%S")

    return render(request, 'about/leader.html', data)


def new_image(name, club, file):
    image = file.get(name)
    image_model = ImageModel(club=club.code, image=image)
    image_model.save()
    return image_model
