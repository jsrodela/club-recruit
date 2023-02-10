from django.urls import path
from . import views

urlpatterns = [
    path("submit/<str:clubname>", views.form),
    path("views/<str:clubname>", views.club)
]
