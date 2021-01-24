from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from game.models import *
from game.forms import *
import random
import json


# Create your views here.
def new_game(request, user_id):
    game = Game(score_sheet={'ones': 1000, 'twos': 1000, 'threes': 1000, 'fours': 1000, 'fives': 1000, 'sixes': 1000,
                             'bonus': 1000, 'upper_sum': 1000,
                             'triple': 1000, 'quadruple': 1000, 'fullhouse': 1000, 'small': 1000, 'big': 1000,
                             'kniffel': 1000, 'chance': 1000, 'lower_sum': 1000, 'final_sum': 1000},
                dice=[1, 1, 1, 1, 1], user=User.objects.get(id=user_id))
    game.save()
    game_id = game.id
    return HttpResponseRedirect(reverse_lazy('roll',
                                             kwargs={'game_id': game_id}))


def roll_dice(request, game_id, dice_to_keep=''):
    that_number = 400
    # Punkte im score_sheet speichern
    if request.method == 'POST' and request.POST.get('points'):
        points = int(request.POST.get('points'))
        print(f' POINTS = {points}')
        game = Game.objects.get(id=game_id)
        game.score_sheet[request.POST.get('category')] = points - that_number
        messages.info(request, f'{points} Punkte gespeichert')
        # Rundenanzahl prüfen und ggf. korrekt setzen
        if game.round % 4 != 0:
            game.round = game.round + (4 - game.round % 4)
        game.save()
        return HttpResponseRedirect(reverse_lazy('roll',
                                                 kwargs={'game_id': game_id}))

    # je nach Punktzahl den User speichern oder löschen, anschließend das Spiel löschen
    if request.method == 'POST' and request.POST.get('finish'):
        game = Game.objects.get(id=game_id)
        score = game.score_sheet['final_sum'] + that_number
        top_users = User.objects.all().order_by('-score')[:5]
        if len(top_users) < 6:
            user = game.user
            user.score = score
            user.save()
        elif score > top_users[4].score:
            top_users[4].delete()
            user = game.user
            user.score = score
            user.save()
        else:
            game.user.delete()
        game.delete()
        return HttpResponseRedirect(reverse_lazy('get_score'))

    # nicht ausgewählte Würfel würfeln und mögliche Punkte berechnen
    if request.method == 'GET':
        game = Game.objects.get(id=game_id)
        dice = game.dice
        scores = json.loads(json.dumps(game.score_sheet))
        print(f'scores: {scores}')
        game.round = game.round + 1
        dice_to_keep = '0'

        if game.round % 4 != 1:
            if request.GET.get('keep_1'):
                dice_to_keep += '1'
            if request.GET.get('keep_2'):
                dice_to_keep += '2'
            if request.GET.get('keep_3'):
                dice_to_keep += '3'
            if request.GET.get('keep_4'):
                dice_to_keep += '4'
            if request.GET.get('keep_5'):
                dice_to_keep += '5'

            print(f'dice: {dice}')

            dice_list = [int(x) for x in dice_to_keep if x.isdigit()]
            print(f'dice_list: {dice_list}')

            for i in range(len(dice)):
                if i + 1 not in dice_list:
                    dice[i] = random.randint(1, 6)

            print(f'dice nach Würfeln: {dice}')
            numbers = count_numbers(dice)

            print(f'numbers: {numbers}')

            for key in scores:
                print(f'scores[{key}]: {scores[key]}')
                if scores[key] == 1000:
                    scores[key] = check_possible_points(game, numbers, key, that_number)

            game.dice = dice
        else:
            for key in ['bonus', 'upper_sum', 'lower_sum', 'final_sum']:
                if scores[key] == 1000:
                    scores[key] = check_possible_points(game, [0, 0, 0, 0, 0, 0], key, that_number)
        game.save()
        print(f'Scores-Variable: {scores}\n score_sheet: {game.score_sheet}')

        images = ['img/die_0.png', 'img/die_1.png', 'img/die_2.png', 'img/die_3.png', 'img/die_4.png', 'img/die_5.png',
                  'img/die_6.png']
        return render(request, 'game/dice.html', {'page_title': 'Würfeln',
                                                  'game': game_id,
                                                  'user': game.user.name,
                                                  'dice': dice,
                                                  'dice_to_keep': dice_to_keep,
                                                  'scores': scores,
                                                  'round': game.round % 4,
                                                  'number': that_number,
                                                  'images': images,
                                                  'upper': [('Einsen', 'ones'), ('Zweien', 'twos'),
                                                            ('Dreien', 'threes'),
                                                            ('Vieren', 'fours'), ('Fünfen', 'fives'),
                                                            ('Sechsen', 'sixes')],
                                                  'lower': [('Drilling', 'triple'), ('Vierling', 'quadruple'),
                                                            ('Full House', 'fullhouse'), ('Kl. Straße', 'small'),
                                                            ('Gr. Straße', 'big'), ('Kniffel', 'kniffel'),
                                                            ('Chance', 'chance')]})


def count_numbers(dice):
    numbers = [0, 0, 0, 0, 0, 0]
    for die in dice:
        numbers[die - 1] += 1
    return numbers


# Berechnet die mögliche Punktzahl für die angegebene Kategorie;
# sind keine Punkte möglich, wird 1000 zurückgegeben
def check_possible_points(game, numbers, category, that_number):
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
        scores = json.loads(json.dumps(game.score_sheet))
        # print(
        # f'1000 not in list: {1000 not in {scores["ones"], scores["twos"], scores["threes"], scores["fours"], scores["fives"], scores["sixes"]}}')
        # prüft, ob alle oberen Kategorien ausgefüllt sind;
        if 1000 not in {scores['ones'], scores['twos'], scores['threes'], scores['fours'], scores['fives'],
                        scores['sixes']}:
            # wenn die Summe der oberen Punkte >= 63, wird der Bonus von 35 Punkten eingetragen
            if sum((scores['ones'], scores['twos'], scores['threes'], scores['fours'], scores['fives'],
                    scores['sixes'], 6 * that_number)) >= 63:
                game.score_sheet['bonus'] = 35 - that_number
                # game.save()
                return 35 - that_number
            else:
                game.score_sheet['bonus'] = -that_number
                return -that_number
    elif category == 'upper_sum' and game.score_sheet['bonus'] != 1000 and \
            game.score_sheet['upper_sum'] == 1000:
        scores = json.loads(json.dumps(game.score_sheet))
        game.score_sheet['upper_sum'] = sum(
            (scores['ones'], scores['twos'], scores['threes'], scores['fours'], scores['fives'], scores['sixes'],
             scores['bonus'])) + 7 * that_number - that_number  # Die -that_number Punkte aller 7 Summanden bereinigen
        return game.score_sheet['upper_sum']
    elif category == 'triple':
        if not (3 in numbers or 4 in numbers or 5 in numbers):
            return points
        points = 0
        for i in range(len(numbers)):
            points += (i + 1) * numbers[i]
    elif category == 'quadruple':
        if not (4 in numbers or 5 in numbers):
            return points
        points = 0
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
        points = 0
        for i in range(len(numbers)):
            points += (i + 1) * numbers[i]
    elif category == 'lower_sum':
        scores = json.loads(json.dumps(game.score_sheet))
        lower_sum = sum((scores['triple'], scores['quadruple'], scores['fullhouse'], scores['small'], scores['big'],
                         scores['kniffel'], scores['chance'], 7 * that_number))
        print(f'lower_sum: {lower_sum}')
        if lower_sum < 1000:
            game.score_sheet['lower_sum'] = lower_sum - that_number
            return lower_sum - that_number
    elif category == 'final_sum':
        final_sum = game.score_sheet['upper_sum'] + game.score_sheet[
            'lower_sum'] + 2 * that_number
        if final_sum < 1000:
            game.score_sheet['final_sum'] = final_sum - that_number
            return final_sum - that_number
    if points == 0:
        return 1000
    return points


def add_user(request):
    user = User()

    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse_lazy('new_game', kwargs={'user_id': new_user.id}))
        else:
            messages.error(request, 'Name ungültig.')
    else:
        form = UsersForm(instance=user)

    return render(request, 'game/add_user.html', {'page_title': 'User hinzufügen',
                                                  'form': form})
