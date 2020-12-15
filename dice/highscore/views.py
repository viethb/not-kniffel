from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def get_score(request):

    return HttpResponse(f'''
    <!DOCTYPE>
    <html>
    <body>
    <p>The highscore will be here</p>
    <p>To play dice go to /game</p>
    </body>
    </html>
    ''')

