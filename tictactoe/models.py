from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class GameRoom(models.Model):
    room_name = models.CharField(max_length=255)
    online = models.ManyToManyField(to=User, blank=True)

    def is_full(self):
        return self.online.count() == 2

    def add_user(self, user):
        if not self.is_full():
            self.online.add(user)
        else:
            raise Exception("Room is full")
        if self.online.count() == 1:
            return "X"
        elif self.online.count() == 2:
            return "O"

    def __str__(self):
        return self.room_name
