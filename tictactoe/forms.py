from django import forms


class CreateRoomForm(forms.Form):
    room_name = forms.CharField(max_length=255)
