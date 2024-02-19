from django.urls import path
from . import views

urlpatterns = [
    path("club_relation", views.club_relation),
]
