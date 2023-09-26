from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("<str:room_name>/", views.room_view, name="chat_room"),
]
