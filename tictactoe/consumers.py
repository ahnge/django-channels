import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import GameRoom


class TicTacToeConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.game_room = None
        self.user = None

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"game_room_{self.room_name}"
        self.game_room = GameRoom.objects.get(room_name=self.room_name)
        self.user = self.scope["user"]

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        # send the user list to the newly joined user
        self.send(
            json.dumps(
                {
                    "type": "user.list",
                    "message": {
                        "users": [
                            user.username for user in self.game_room.online.all()
                        ],
                    },
                    "event": "userList",
                }
            )
        )

    def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.game_room.online.remove(self.user)
        # Send updated players list to the channel group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "send_message",
                "message": {
                    "users": [user.username for user in self.game_room.online.all()]
                },
                "event": "userLeave",
            },
        )
        print("did this ran?")

    def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)

        if event == "MOVE":
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "send_message", "message": message, "event": "MOVE"},
            )

        if event == "JOIN":
            if not self.user.is_authenticated:
                return

            char_choice = self.game_room.add_user(self.user)

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "send_message",
                    "message": {
                        "game_can_start": self.game_room.is_full(),
                        "users": [
                            user.username for user in self.game_room.online.all()
                        ],
                    },
                    "event": "JOIN",
                },
            )
            # Set char choice for that user in client
            self.send(
                json.dumps(
                    {
                        "type": "set.char_choice",
                        "message": {
                            "char_choice": char_choice,
                        },
                        "event": "setCharChoice",
                    }
                )
            )

        if event == "START":
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "send_message", "message": message, "event": "START"},
            )

        if event == "END":
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "send_message", "message": message, "event": "END"},
            )

    def send_message(self, res):
        """Receive message from room group"""
        # Send message to WebSocket
        self.send(text_data=json.dumps(res))

    def user_list(self, res):
        """Receive message from room group"""
        # Send message to WebSocket
        self.send(text_data=json.dumps(res))

    def set_char_choice(self, res):
        """Receive message from room group"""
        # Send message to WebSocket
        self.send(text_data=json.dumps(res))
