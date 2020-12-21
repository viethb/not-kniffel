from django.db import models
import jsonfield
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30)
    score = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f'{self.name}, max: {self.score}'


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score_sheet = jsonfield.JSONField()
    dice = jsonfield.JSONField()
