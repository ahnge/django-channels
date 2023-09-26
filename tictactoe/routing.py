from .consumers import TicTacToeConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r"^ws/play/(?P<room_name>\w+)/$", TicTacToeConsumer.as_asgi()),
]
