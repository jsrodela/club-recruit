from django.contrib import auth


def get_data(request):
    user = auth.get_user(request)
    if user.is_authenticated:
        return {'user': user}
    else:
        return {}
