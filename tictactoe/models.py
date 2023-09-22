from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class GameRoom(models.Model):
    room_name = models.CharField(max_length=255)
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="room1", null=True, blank=True
    )
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="room2", null=True, blank=True
    )

    def is_full(self):
        return self.user1 is not None and self.user2 is not None

    def add_user(self, user):
        if self.user1 is None:
            self.user1 = user
            return "X"
        elif self.user2 is None:
            self.user2 = user
            return "O"
        else:
            raise Exception("Room is full")

    def __str__(self):
        return self.room_name
