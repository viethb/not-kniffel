"""dice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from highscore.views import *
from game.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/new/<int:user_id>/', new_game, name='new_game'),
    path('game/<int:game_id>/<str:dice_to_keep>', roll_dice, name='roll2'),
    path('game/<int:game_id>/', roll_dice, name='roll'),
    path('game/add-user/', add_user, name='add_user'),
    path('', get_score, name='get_score')
]
