from django.urls import path
from . import views

urlpatterns = [
    path("club_config", views.club_config),
    path("view_forms", views.view_forms),
]
