from django.forms import *
from game.models import *


class UsersForm(ModelForm):
    class Meta:
        model = User
        exclude = ('score',)
        labels = {'name': 'Name'}
