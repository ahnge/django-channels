from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


from .models import GameRoom
from .forms import CreateRoomForm, CustomUserCreationForm


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("ttt:index")
        return render(request, "registration/register.html", {"form": form})
    elif request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("ttt:index")
        else:
            form = AuthenticationForm(request.POST)
            return render(
                request,
                "registration/login.html",
                {
                    "form": form,
                    "error": "Please enter a correct username and password.",
                },
            )
    elif request.method == "GET":
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("ttt:login")


# Create your views here.
def index(request):
    game_rooms = None
    if request.user.is_authenticated:
        game_rooms = GameRoom.objects.all()
    context = {"game_rooms": game_rooms}
    return render(request, "tictactoe/index.html", context)


@login_required
def game_room(request, room_id):
    game_room = GameRoom.objects.get(pk=room_id)
    game_room.add_user(request.user)
    game_room.save()

    context = {"game_room": game_room}
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
            if len(int(room_name)) == 0:
                messages.error(request, "You need to provide the room name.")
                return redirect("ttt:index")
            else:
                # Create a new room
                room = GameRoom(room_name=room_name)
                room.save()
            return redirect("ttt:game_room", room_id=room.id)
    return redirect("ttt:index")
