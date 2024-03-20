from django.contrib import auth

from about.models import ClubModel


def get_data(request):
    data = {}

    user = auth.get_user(request)
    if user.is_authenticated:
        data['user'] = user
    else:
        pass

    clubs = []
    for club in ClubModel.objects.all().order_by('end', 'name'):
        obj = {
            'name': club.name,
            'code': club.code,
            'end': club.end
        }
        if club.logo_image is not None:
            obj['logo_url'] = club.logo_image.image.url
        clubs.append(obj)
    data['clubs'] = clubs

    return data
