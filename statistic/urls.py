from django.urls import path
from .views import *

urlpatterns = [
    path('home/', show_main_page, name='home'),
    path('player/<str:player_name>/', show_player, name='player'),
    path('team/<str:team_name>/', show_team),
    path('statistika/', show_smth, name='statistika'),
]

