from django import template

register = template.Library()


@register.filter(name='get_index')
def get_index(array, index):
    try:
        return array[index]
    except:
        return None


@register.filter(name='get_score')
def get_score(scores, pair):
    try:
        return scores[pair[1]]
    except:
        return None
