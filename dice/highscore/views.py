from django.shortcuts import render
from django.http import HttpResponse
from game.models import *

# Create your views here.


def get_score(request):
    user_list = User.objects.all().order_by('-score')[:5]
    return render(request, 'highscore/landing.html', {'page_title': 'Nicht Kniffel',
                                                      'users': user_list})

