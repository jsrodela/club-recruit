from django.shortcuts import render, redirect

from about.models import ClubModel
from account.base import get_data


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
        print(request.POST)

        pass
    data['club_form_start'] = club.form_start.strftime("%Y-%m-%dT%H:%M:%S")
    data['club_form_end'] = club.form_end.strftime("%Y-%m-%dT%H:%M:%S")

    return render(request, 'about/leader.html', data)
