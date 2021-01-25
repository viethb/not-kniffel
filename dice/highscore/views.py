from django.shortcuts import render
from game.models import *


def get_score(request):
    # Gibt die fünf Spieler mit den höchsten Punktzahlen zurück
    user_list = User.objects.all().order_by('-score')[:5]
    return render(request, 'highscore/landing.html', {'page_title': 'Nicht Kniffel',
                                                      'users': user_list})

