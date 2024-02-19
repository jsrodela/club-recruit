from django.shortcuts import render
from account.base import get_data

# Create your views here.

def club_relation(request):
    data = get_data(request)
    return render(request, 'notice/clubRelation.html', data)
