from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import GameRoom


# Create your views here.
def index(request):
    game_rooms = None
    if request.user.is_authenticated:
        game_rooms = GameRoom.objects.all()
    context = {"game_rooms": game_rooms}
    return render(request, "tictactoe/index.html", context)


@login_required
def game_room(request, room_name):
    game_room, created = GameRoom.objects.get_or_create(room_name=room_name)

    context = {"game_room": game_room}
    return render(request, "tictactoe/game_room.html", context)
