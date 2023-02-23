from django.urls import path
from . import views

urlpatterns = [
    path("<str:clubname>/", views.about),
]
