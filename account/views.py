from django.shortcuts import render


def login(request):
    if request.POST:
        pass
    return render(request, 'account/login.html', {})
