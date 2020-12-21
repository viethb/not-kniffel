from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from game.models import *
from game.forms import *
import random


# Create your views here.
def new_game(request):
    game = Game(score_sheet={'ones': -1, 'twos': -1, 'threes': -1, 'fours': -1, 'fives': -1, 'sixes': -1, 'triple': -1,
                             'quadruple': -1, 'fullhouse': -1, 'small': -1, 'big': -1, 'kniffel': -1, 'chance': -1},
                dice=[1, 1, 1, 1, 1], user=User.objects.get(id=1))
    game.save()
    game_id = game.id
    return render(request, 'game/dice.html', {'page_title': 'Würfeln',
                                              'game': game_id,
                                              'dice': game.dice,
                                              'scores': game.score_sheet})


def roll_dice(request, game_id, dice_to_keep=''):
    game = Game.objects.get(id=game_id)
    dice = game.dice
    scores = dict(game.score_sheet)

    print(scores)
    print(dice)

    dice_list = [int(x) for x in dice_to_keep if x.isdigit()]
    print(dice_list)

    for i in range(len(dice)):
        if i + 1 not in dice_list:
            dice[i] = random.randint(1, 6)

    numbers = count_numbers(dice)

    for key in scores:
        if scores[key] == -1:
            scores[key] = check_possible_points(numbers, key)

    game.dice = dice
    game.save()
    print(f'Scores-Variable: {scores}\n score_sheet: {game.score_sheet}')
    return render(request, 'game/dice.html', {'page_title': 'Würfeln',
                                              'game': game_id,
                                              'dice': dice,
                                              'scores': scores})
    # return render(request, 'game/dice.html', {'page_title': 'Würfeln',
    #                                           'dice': self.dice,
    #                                           'scores': scores})


def count_numbers(dice):
    numbers = [0, 0, 0, 0, 0, 0]
    for die in dice:
        numbers[die - 1] += 1
    return numbers


# Berechnet die mögliche Punktzahl für die angegebene Kategorie;
# sind keine Punkte möglich, wird -1 zurückgegeben
def check_possible_points(numbers, category):
    points = -1
    if category == 'ones':
        points = numbers[0] * 1
    elif category == 'twos':
        points = numbers[1] * 2
    elif category == 'threes':
        points = numbers[2] * 3
    elif category == 'fours':
        points = numbers[3] * 4
    elif category == 'fives':
        points = numbers[4] * 5
    elif category == 'sixes':
        points = numbers[5] * 6
    elif category == 'triple':
        if not (3 in numbers or 4 in numbers or 5 in numbers):
            return points
        for i in range(len(numbers)):
            points += (i + 1) * numbers[i]
    elif category == 'quadruple':
        print(f'In quadruple, numbers = {numbers}')
        if not (4 in numbers or 5 in numbers):
            return points
        for i in range(len(numbers)):
            points += (i + 1) * numbers[i]
    elif category == 'fullhouse':
        if 2 in numbers and 3 in numbers:
            return 25
    elif category == 'small':
        if numbers.count(0) <= 2 and \
                (numbers[0] in (1, 2) and numbers[1] in (1, 2) and numbers[2] in (1, 2) and numbers[3] in (1, 2)
                 or numbers[1] in (1, 2) and numbers[2] in (1, 2) and numbers[3] in (1, 2) and numbers[4] in (1, 2)
                 or numbers[2] in (1, 2) and numbers[3] in (1, 2) and numbers[4] in (1, 2) and numbers[5]) in (
                1, 2):
            return 30
    elif category == 'big':
        if numbers.count(0) <= 1 and \
                (numbers[0] == numbers[1] == numbers[2] == numbers[3] == numbers[4]
                 or numbers[1] == numbers[2] == numbers[3] == numbers[4] == numbers[5]):
            return 40
    elif category == 'kniffel':
        if 5 in numbers:
            return 50
    elif category == 'chance':
        for i in range(len(numbers)):
            points += (i + 1) * numbers[i]
    if points == 0:
        return -1
    return points


# class Game:

# def __init__(self):
#     self.dice = [1, 1, 1, 1, 1]
#     self.scores = {'ones': 0, 'twos': 0, 'threes': 0, 'fours': 0, 'fives': 0, 'sixes': 0, 'triple': 0,
#                    'quadruple': 0, 'fullhouse': 0, 'small': 0, 'big': 0, 'kniffel': 0, 'chance': 0}
#
# def get_dice(self, request, dice_to_keep=''):
#
#     print(self.dice)
#
#     dice_list = [int(x) for x in dice_to_keep if x.isdigit()]
#     print(dice_list)
#     time_delta = {
#         'CET': 0,
#         'BRT': -4,
#         'CDT': -5,
#         'GMT': -1,
#     }
#
#     for i in range(len(self.dice)):
#         if i + 1 not in dice_list:
#             self.dice[i] = random.randint(1, 6)
#
#     numbers = self.count_numbers()
#
#     for key in self.scores:
#         self.scores[key] = self.check_possible_points(numbers, key)
#
#     # return render(request, 'game/dice.html', {'page_title': 'Würfeln',
#     #                                           'dice': self.dice,
#     #                                           'scores': scores})
#
# def count_numbers(self):
#     numbers = [0, 0, 0, 0, 0, 0]
#     for die in self.dice:
#         numbers[die - 1] += 1
#     return numbers
#
# def check_possible_points(self, numbers, category):
#     points = 0
#     if category == 'ones':
#         points = numbers[0] * 1
#     elif category == 'twos':
#         points = numbers[1] * 2
#     elif category == 'threes':
#         points = numbers[2] * 3
#     elif category == 'fours':
#         points = numbers[3] * 4
#     elif category == 'fives':
#         points = numbers[4] * 5
#     elif category == 'sixes':
#         points = numbers[5] * 6
#     elif category == 'triple':
#         if not (3 in numbers or 4 in numbers or 5 in numbers):
#             return points
#         for i in range(len(numbers)):
#             points += (i + 1) * numbers[i]
#     elif category == 'quadruple':
#         print(f'In quadruple, numbers = {numbers}')
#         if not (4 in numbers or 5 in numbers):
#             return points
#         for i in range(len(numbers)):
#             points += (i + 1) * numbers[i]
#     elif category == 'fullhouse':
#         if 2 in numbers and 3 in numbers:
#             return 25
#     elif category == 'small':
#         if numbers.count(0) <= 2 and \
#                 (numbers[0] in (1, 2) and numbers[1] in (1, 2) and numbers[2] in (1, 2) and numbers[3] in (1, 2)
#                  or numbers[1] in (1, 2) and numbers[2] in (1, 2) and numbers[3] in (1, 2) and numbers[4] in (1, 2)
#                  or numbers[2] in (1, 2) and numbers[3] in (1, 2) and numbers[4] in (1, 2) and numbers[5]) in (
#         1, 2):
#             return 30
#     elif category == 'big':
#         if numbers.count(0) <= 1 and \
#                 (numbers[0] == numbers[1] == numbers[2] == numbers[3] == numbers[4]
#                  or numbers[1] == numbers[2] == numbers[3] == numbers[4] == numbers[5]):
#             return 40
#     elif category == 'kniffel':
#         if 5 in numbers:
#             return 50
#     elif category == 'chance':
#         for i in range(len(numbers)):
#             points += (i + 1) * numbers[i]
#     return points


def add_user(request):
    user = User()

    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User gespeichert.')
            return HttpResponseRedirect(reverse_lazy('get_score'))
        else:
            messages.error(request, 'Name ungültig.')
    else:
        form = UsersForm(instance=user)

    return render(request, 'game/add_user.html', {'page_title': 'User hinzufügen',
                                                  'form': form})
