from django.forms import ModelForm, fields
from .models import Room,Message


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude=['host','participants']



class messageForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"