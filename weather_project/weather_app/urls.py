from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('current/', views.current_view, name='current'),
    path('forecast/', views.forcast_view, name='forecast'),
    path('specific/', views.specific_view, name='specific'),
]