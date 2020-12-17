from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.

dice = [1, 1, 1, 1, 1]


def get_dice(request, dice_to_keep=''):
    global dice

    print(dice)

    dice_list = [int(x) for x in dice_to_keep if x.isdigit()]
    print(dice_list)
    time_delta = {
        'CET': 0,
        'BRT': -4,
        'CDT': -5,
        'GMT': -1,
    }

    for i in range(len(dice)):
        if i + 1 not in dice_list:
            dice[i] = random.randint(1, 6)

    numbers = count_numbers()
    scores = {'ones': 0, 'twos': 0, 'threes': 0, 'fours': 0, 'fives': 0, 'sixes': 0, 'triple': 0, 'quadruple': 0,
              'fullhouse': 0, 'small': 0, 'big': 0, 'kniffel': 0, 'chance': 0}

#   possibilities = f'''
#     <table>
#   <tr>
#     <th>Einsen</th>
#     <td>{numbers[0] * 1}</td>
#   </tr>
#   <tr>
#     <th>Zweien</th>
#     <td>{numbers[1] * 2}</td>
#   </tr>
#   <tr>
#     <th>Dreien</th>
#     <td>{numbers[2] * 3}</td>
#   </tr>
# <tr>
#     <th>Vieren</th>
#     <td>{numbers[3] * 4}</td>
#   </tr>
# <tr>
#     <th>Fünfen</th>
#     <td>{numbers[4] * 5}</td>
#   </tr>
# <tr>
#     <th>Sechsen</th>
#     <td>{numbers[5] * 6}</td>
#   </tr>
# <tr>
#     <th>Drilling</th>
#     <td>{check_possible_points(numbers, 'Triple')}</td>
#   </tr>
# <tr>
#     <th>Vierling</th>
#     <td>{check_possible_points(numbers, 'Quadruple')}</td>
#   </tr>
# <tr>
#     <th>Full House</th>
#     <td>{check_possible_points(numbers, 'FullHouse')}</td>
#   </tr>
# <tr>
#     <th>Kl. Straße</th>
#     <td>{check_possible_points(numbers, 'small')}</td>
#   </tr>
# <tr>
#     <th>Gr. Straße</th>
#     <td>{check_possible_points(numbers, 'big')}</td>
#   </tr>
# <tr>
#     <th>Kniffel</th>
#     <td>{check_possible_points(numbers, 'Kniffel')}</td>
#   </tr>
# <tr>
#     <th>Chance</th>
#     <td>{check_possible_points(numbers, 'Chance')}</td>
#   </tr>
# </table>
#    '''

    # return HttpResponse(f'''
    # <!DOCTYPE>
    # <html>
    # <body>
    # {dice}
    # {possibilities}
    # </body>
    # </html>
    # ''')

    for key in scores:
        scores[key] = check_possible_points(numbers, key)

    return render(request, 'game/dice.html', {'page_title': 'Würfeln',
                                              'dice': dice,
                                              'scores': scores})


def count_numbers():
    numbers = [0, 0, 0, 0, 0, 0]
    for die in dice:
        numbers[die - 1] += 1
    return numbers


def check_possible_points(numbers, category):
    points = 0
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
                 or numbers[2] in (1, 2) and numbers[3] in (1, 2) and numbers[4] in (1, 2) and numbers[5]) in (1, 2):
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
    return points
