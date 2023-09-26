from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import GameRoom
from .forms import CreateRoomForm


# Create your views here.
def index(request):
    game_rooms = None
    if request.user.is_authenticated:
        game_rooms = GameRoom.objects.all()
    context = {"game_rooms": game_rooms}
    return render(request, "tictactoe/index.html", context)


@login_required
def game_room(request, room_name):
    game_room = GameRoom.objects.get(room_name=room_name)
    # If the user has already joined the room, reconnect
    if game_room.user1 == request.user:
        context = {"game_room": game_room, "char_choice": "X"}
        return render(request, "tictactoe/game_room.html", context)
    elif game_room.user2 == request.user:
        context = {"game_room": game_room, "char_choice": "O"}
        return render(request, "tictactoe/game_room.html", context)
    # Ensure the room is not full
    if game_room.is_full():
        messages.error(request, "Oops! The room is full.")
        return redirect("ttt:index")
    # User is new
    char_choice = game_room.add_user(request.user)
    game_room.save()

    context = {"game_room": game_room, "char_choice": char_choice}
    return render(request, "tictactoe/game_room.html", context)


@login_required
def create_game(request):
    if request.method == "POST":
        form = CreateRoomForm(request.POST)

        if form.is_valid():
            room_name = form.cleaned_data["room_name"]
            room = None

            # Check if a room with the same name already exists
            existing_room = GameRoom.objects.filter(room_name=room_name).first()
            if existing_room:
                messages.error(request, "The room with that name already exists.")
                return redirect("ttt:index")
            # Ensure room name is not empty
            if not len(room_name) > 0:
                messages.error(request, "You need to provide the room name.")
                return redirect("ttt:index")
            else:
                # Create a new room
                room = GameRoom(room_name=room_name)
                room.save()
            return redirect("ttt:game_room", room_name=room_name)
    return redirect("ttt:index")
