from django.urls import path
from . import views

urlpatterns = [
    path("submit/<str:clubname>", views.form),
    path("example_form/", views.example_form),
]
