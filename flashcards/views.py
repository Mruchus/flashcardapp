from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django import forms
from django.http import HttpResponse, Http404
from .models import Card, Review
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)

# class-based view -> allows you to display a list or detail page for a model


def hello(request):
    return HttpResponse("Hello, World!")

def display_text_file(request):
    with open('flashcards/test.txt', 'r') as f:
        file_content = f.read()
    return HttpResponse(file_content)

def display_cards(request):
    cards = Card.objects.all() # retrieves all the Card obejcts from the database
    return render(request, 'cards.html', {'cards': cards}) # renders using the cards template

def card_detail(request, card_id):
    num_cards = Card.objects.count()
    try:
        # get card based on pk
        card = Card.objects.get(pk=card_id)
        # get a collection of all card objects
        cards = Card.objects.all()

        # find the index of the card
        for index, obj in enumerate(cards):
            if obj == card:
                current_i = index
        
        start_of_cards = False
        end_of_cards = False
        
        if current_i == 0: # start of cards so no card before
            start_of_cards = True
            previous_id = None
            next_id = cards[current_i+1].id

        if current_i == num_cards - 1: # last card so no more cards afterwards
            end_of_cards = True
            previous_id = cards[current_i-1].id
            next_id = None
        
        elif current_i != 0: # card in the middle
            previous_id = cards[current_i-1].id
            next_id = cards[current_i+1].id

    except Card.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'card_detail.html',
    {'card': card, 'num_of_cards':num_cards,
    'previous_id': previous_id, 'next_id': next_id,
    'start_of_cards': start_of_cards, 'end_of_cards': end_of_cards})

# form to add new flashcards
class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer",] # fields for the form

    # after form successfully completed, return to creating more cards
    success_url = reverse_lazy("create_card") 

    def get_context_data(self, **kwargs): 
        'add additional context variables to the template context'
        context = super().get_context_data(**kwargs) # get the default context data from the parent class
        context['num_cards'] = Card.objects.count()

        # get the id of the previously created card
        context['last_id'] = Card.objects.all().last().id
        return context

# form to edit flashcards
class CardUpdateView(CardCreateView, UpdateView):
    model = Card
    # speicify what template to use when rendering the view
    template_name = 'flashcards/card_form.html'

    def get_success_url(self):
        return reverse_lazy('display_card', kwargs={'card_id': self.object.pk}) # gets the id of the current card

class CardDeleteView(DeleteView): #looks for card_confirm_delete.html
    model = Card
    template_name = 'flashcards/card_confirm_delete.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) # get the default context data from the parent class
        # get the id of the current card
        context['current_id'] = self.object.pk
        return context

    # return to previous card
    def get_success_url(self):
        card = self.object
        cards = Card.objects.all()

        # get id of previous card
        for index, obj in enumerate(cards):
            if obj == card:
                current_i = index
        previous_id = cards[current_i-1].id

        return reverse_lazy('display_card', kwargs={'card_id': previous_id}) # gets the id of the previous card

# determine which flashcards need to be reviewed
def review(request):

    # Query the database for all flashcards that have a review scheduled for today or earlier
    # flashcard_to_review = Card.objects.annotate(
    # latest_review=Max('review__scheduled')).filter( # get lastest scheduled for each card
    #     review__scheduled__lte=timezone.now() # get cards with review time earlier than now
    # ).order_by('review__scheduled').first() # get the first card

    # after finish review
    if request.method == 'POST':
        review_id = request.POST.get('review_id','')
        review = Review.objects.get(pk=review_id)
        
        # Get the current time
        now = timezone.now()
        review.completed = now
        review.save()

        new_scheduled = None
        # Update the scheduled time based on which button was clicked
        if 'one' in request.POST:
            print('one')
            new_scheduled = now + timezone.timedelta(minutes=1)
        elif 'ten' in request.POST:
            print('ten')
            new_scheduled = now + timezone.timedelta(minutes=10)
        elif 'four' in request.POST:
            print('four')
            new_scheduled = now + timezone.timedelta(days=4)  # approximately one month

        # Update the object in the database
        review = Review.objects.create(flashcard=review.flashcard, scheduled=new_scheduled)
        review.save()

        # finish one card move onto the next
        return redirect('review')

    else: # GET 
        earliest_scheduled_review = Review.objects.filter(completed__isnull=True).order_by('scheduled').first()
        flashcard = earliest_scheduled_review.flashcard
        
        #maybe don't need this, just have completed
        earliest_scheduled_review.started = timezone.now()
        earliest_scheduled_review.save()
        
        # Render the review template, passing in the flashcards to review
        return render(request, 'review.html', {'card': flashcard, 'review': earliest_scheduled_review})

def finish_review(request, card_id):
    # Get the flashcard being reviewed (faster function than try and except)
    flashcard = get_object_or_404(Card, pk=card_id)

    # Check if the user got the flashcard correct
    break_time = request.POST.get('break_time')

    # Create a new Review instance with the current date and result
    review = Review(flashcard=flashcard, time=timezone.now(), result=break_time)
    review.save()

    # Schedule the next review 
    if break_time == 1: # schedule review for next minute
        flashcard.review.date = timezone.now() + timezone.timedelta(minutes=1)
    elif break_time == 10: # schedule for in 10 mins
        flashcard.review.date = timezone.now() + timezone.timedelta(minutes=10)
    else: # scedule for in 4 days
        flashcard.review.date = timezone.now() + timezone.timedelta(days=4)
    flashcard.save()

    # Redirect the user back to the review page
    return redirect('review')


