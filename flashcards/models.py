from django.db import models

# create a model of the flashcard
class Card(models.Model):
    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)
    points = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.question}'

# review class to keep track of when the card should next be displayed
class Review(models.Model):
    # link Review instances with Card instances using a foreign key
    flashcard = models.ForeignKey(Card, on_delete=models.CASCADE) 
    # if flashcard is deleted, obejct withforeign key is also deleted

    # time to review
    scheduled = models.DateTimeField()
    # time viewed
    started = models.DateTimeField(blank=True, null=True)
    # time finished
    completed = models.DateTimeField(blank=True, null=True)

# header for when appearing in the database
def __str__(self) -> str:
        return f'Review({self.scheduled}, {self.started}, {self.completed})'


