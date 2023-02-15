from django.urls import path
from . import views

urlpatterns = [
    path("leader", views.leader),
    path("<str:clubname>/", views.about),
]
