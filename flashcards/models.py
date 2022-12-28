from django.db import models

from django.db import models


# create a model of the flashcard
class Card(models.Model):
    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)
    points = models.IntegerField(default=1)


    def __str__(self) -> str:
        return f'{self.question}'