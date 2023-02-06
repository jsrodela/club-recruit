from django.urls import path
from . import views

urlpatterns = [
    path("", views.form),
    path("example_form/", views.example_form),
]
