from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Card
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
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
        card = Card.objects.get(pk=card_id)
        cards = Card.objects.all()
        #print(cards)
        for index, obj in enumerate(cards):
            if obj == card:
                current_i = index
        
        start_of_cards = False
        end_of_cards = False
        
        if current_i == 0:
            start_of_cards = True
            previous_id = None
            next_id = cards[current_i+1].id

        if current_i == num_cards - 1:
            end_of_cards = True
            previous_id = cards[current_i-1].id
            next_id = None
        
        elif current_i != 0:
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
    fields = ["question", "answer"] # fields for the form
    # after form successfully completed, return to creating more cards
    success_url = reverse_lazy("create_card") 

    def get_context_data(self, **kwargs): 
        'add additional context variables to the template context'
        context = super().get_context_data(**kwargs) # get the default context data from the parent class
        context['num_cards'] = Card.objects.count()

        # get the id of the previously created card
        context['last_id'] = Card.objects.all().last().id
        return context






