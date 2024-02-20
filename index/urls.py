from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("club_relation", views.club_relation),
]
