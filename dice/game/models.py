from django.db import models
# import jsonfield
# Create your models here.
# from django.contrib.postgres.fields import JSONField

from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Bitte nur Buchstaben und Zahlen eingeben')


class User(models.Model):
    name = models.CharField(max_length=30, validators=[alphanumeric])
    score = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f'{self.name}, Punkte: {self.score}'


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score_sheet = models.JSONField()
    dice = models.JSONField()
    round = models.IntegerField(default=0)
