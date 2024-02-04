from django.urls import path
from . import views

urlpatterns = [
    path("submit/<str:clubname>", views.form),
    path("views/<str:clubname>", views.club),
    path("leader/<int:form_id>", views.leader_view),
    path("time/<str:clubname>", views.time),
    path("cancel/<str:clubname>", views.cancel)
]
