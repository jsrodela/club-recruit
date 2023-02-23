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

