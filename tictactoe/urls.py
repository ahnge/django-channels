from django.urls import path

from . import views

app_name = "ttt"

urlpatterns = [
    path("", views.index, name="index"),
    path("create-game", views.create_game, name="create_game"),
    path("<str:room_name>/", views.game_room, name="game_room"),
]
