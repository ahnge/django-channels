from django.urls import path

from . import views

app_name = "ttt"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("create-game", views.create_game, name="create_game"),
    path("<int:room_id>/", views.game_room, name="game_room"),
]
