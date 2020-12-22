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
    game = Game(score_sheet={'ones': 1000, 'twos': 1000, 'threes': 1000, 'fours': 1000, 'fives': 1000, 'sixes': 1000,
                             'bonus': 1000, 'upper_sum': 1000,
                             'triple': 1000, 'quadruple': 1000, 'fullhouse': 1000, 'small': 1000, 'big': 1000,
                             'kniffel': 1000, 'chance': 1000, 'lower_sum': 1000, 'final_sum': 1000},
                dice=[1, 1, 1, 1, 1], user=User.objects.get(id=1))
    game.save()
    game_id = game.id
    return HttpResponseRedirect(reverse_lazy('roll',
                                             kwargs={'game_id': game_id}))
    # return render(request, 'game/dice.html', {'page_title': 'Würfeln',
    #                                           'game': game_id,
    #                                           'dice': game.dice,
    #                                           'dice_to_keep': 12345,
    #                                           'scores': game.score_sheet,
    #                                           'round': game.round % 4})


def roll_dice(request, game_id, dice_to_keep=''):
    if request.method == 'POST' and request.POST.get('points'):
        points = int(request.POST.get('points'))
        print(f' POINTS = {points}')
        game = Game.objects.get(id=game_id)
        game.score_sheet[request.POST.get('category')] = points - 300
        # Rundenanzahl prüfen und ggf. korrekt setzen
        if game.round % 4 != 0:
            game.round = game.round + (4 - game.round % 4)
        game.save()
        messages.success(request, f'Points = {points}')
        return HttpResponseRedirect(reverse_lazy('roll',
                                                 kwargs={'game_id': game_id}))

    if request.method == 'GET' and request.GET.get('roll'):
        dice_to_keep = request.GET.get('dice_to_keep')
        dice_to_keep = dice_to_keep if dice_to_keep is not None else '0'

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
        if scores[key] == 1000:
            scores[key] = check_possible_points(game, numbers, key)

    if request.method == 'GET':
        game.round = game.round + 1
    game.dice = dice
    game.save()
    print(f'Scores-Variable: {scores}\n score_sheet: {game.score_sheet}')
    return render(request, 'game/dice.html', {'page_title': 'Würfeln',
                                              'game': game_id,
                                              'dice': dice,
                                              'dice_to_keep': dice_to_keep,
                                              'scores': scores,
                                              'round': game.round % 4})


def count_numbers(dice):
    numbers = [0, 0, 0, 0, 0, 0]
    for die in dice:
        numbers[die - 1] += 1
    return numbers


# Berechnet die mögliche Punktzahl für die angegebene Kategorie;
# sind keine Punkte möglich, wird 1000 zurückgegeben
def check_possible_points(game, numbers, category):
    points = 1000
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
    elif category == 'bonus':
        print('In bonus')
        scores = game.score_sheet
        print(f'Scores: {scores}')
        print(f'100 in list: {1000 not in {scores["ones"], scores["twos"], scores["threes"], scores["fours"], scores["fives"],scores["sixes"]}}')
        if 1000 not in {scores['ones'], scores['twos'], scores['threes'], scores['fours'], scores['fives'],
                        scores['sixes']}:
            if sum((scores['ones'], scores['twos'], scores['threes'], scores['fours'], scores['fives'],
                    scores['sixes'])) >= 63:
                game.score_sheet['bonus'] = 35 -300
                #game.save()
                return 35
            else:
                game.score_sheet['bonus'] = -300
                return -300
    elif category == 'upper_sum' and game.score_sheet['bonus'] != 1000:
        scores = game.score_sheet
        game.score_sheet['upper_sum'] = sum(
            (scores['ones'], scores['twos'], scores['threes'], scores['fours'], scores['fives'], scores['sixes'],
             scores['bonus'])) + 2100 - 300 # Die -300 Punkte aller 7 Summanden bereinigen
        return game.score_sheet['upper_sum'] + 2100 - 300
    elif category == 'triple':
        if not (3 in numbers or 4 in numbers or 5 in numbers):
            return points
        for i in range(len(numbers)):
            points += (i + 1) * numbers[i]
    elif category == 'quadruple':
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
    elif category == 'lower_sum':
        scores = game.score_sheet
        lower_sum = sum((scores['triple'], scores['quadruple'], scores['fullhouse'], scores['small'], scores['big'],
                        scores['kniffel'], scores['chance']))
        if lower_sum < 1000:
            game.score_sheet['lower_sum'] = lower_sum
            return 0
    elif category == 'final_sum':
        final_sum = game.score_sheet['upper_sum'] + game.score_sheet['lower_sum']
        if final_sum < 1000:
            game.score_sheet['final_sum'] = final_sum
            return final_sum
    if points == 0:
        return 1000
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
#         'GMT': 1000,
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
