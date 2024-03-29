from django.urls import path
from . import views

urlpatterns = [
    path("club_config", views.club_config),
    path("view_forms", views.view_forms),
    path("time_config", views.time_config),
    path("first_result", views.first_result),
    path("every_forms", views.every_forms),
    path("view_time", views.view_time),
    path("second_result", views.second_result),
    path("second_result_check_user", views.second_result_check_user),
    path("additional_result", views.additional_result),
    path("view_selection", views.view_selection),
    path("give_up_all", views.give_up_all),
    path("final_stats", views.final_stats)
]
