from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def get_score(request):
    return render(request, 'highscore/landing.html', {'page_title': 'Nicht Kniffel'})

