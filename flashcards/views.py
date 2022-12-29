from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Card
from django.views import generic
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
    card_num = len(Card.objects.all())
    try:
        card = Card.objects.get(pk=card_id)
    except Card.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'card_detail.html', {'card': card})



