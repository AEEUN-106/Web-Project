from django.urls import path
from . import views

urlpatterns = [
    path('',views.post_list, name = 'post_list'),
    path('data_process/',views.data_process, name = "data_process"),
    path('sorting/',views.sorting, name = "sorting"),
]
