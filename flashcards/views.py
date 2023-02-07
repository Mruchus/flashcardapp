from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django import forms
from django.http import HttpResponse, Http404
from .models import Card, Review
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)

from .forms import LoginForm, NewUserForm

# class-based view -> allows you to display a list or detail page for a model

def logout_view(request):    
    logout(request)

def hello(request):
    return HttpResponse("Hello, World!")

def display_text_file(request):
    with open('flashcards/test.txt', 'r') as f:
        file_content = f.read()
    return HttpResponse(file_content)

def display_cards(request):
    cards = Card.objects.all() # retrieves all the Card obejcts from the database
    return render(request, 'cards.html', {'cards': cards}) # renders using the cards template

def signup(request):
    if request.method == 'POST':
        # populate form fields
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # sucess
            return redirect('home')
    else:
        # retry with error message
        form = NewUserForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
            failed = False
            # populate form fields
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                # check for correct username password combination
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    # user found
                    login(request, user)
                    return redirect('home')
                else:
                    login_form = LoginForm()
                    failed = True
                    return render(request, 'login.html', {'form': login_form, 'failed': failed})
    else:
        # render login page if failed
        failed = False
        login_form = LoginForm()
        return render(request, 'login.html', {'form': login_form, 'failed': failed})

def home(request):    
    # already signed in
    if request.user.is_authenticated:   
        print('User', request.user) 
        first_id = Card.objects.all().filter(user=request.user).first().id
        # get last three cards
        cards = Card.objects.filter(user=request.user).order_by('-id')[:3]

        #print("the first id is", first_id)
        return render(request, 'home.html', {'first_id': first_id, 'cards' : cards, 'user': request.user})
    else:
        # go to login page to sign in
        return redirect('login')

def card_detail(request, card_id):
    #print("the card id is", card_id)
    num_cards = Card.objects.filter(user=request.user).count()
    first_id = Card.objects.all().filter(user=request.user).first().id
    last_id = Card.objects.all().filter(user=request.user).last().id
    try:
        # get card based on pk
        card = Card.objects.filter(user=request.user).get(pk=card_id)
        # get a collection of all card objects
        cards = Card.objects.filter(user=request.user).all()

        # find the index of the card
        for index, obj in enumerate(cards):
            if obj == card:
                current_i = index
        
        start_of_cards = False
        end_of_cards = False

        print("this is the card, first and last id", card_id, first_id, last_id)
        if card_id == first_id: # start of cards so no card before
            start_of_cards = True
            previous_id = None
            try:
                next_id = cards[current_i+1].id
            except:
                end_of_cards = True
                # only one card
                next_id = None

        elif card_id == last_id: # last card so no more cards afterwards
            end_of_cards = True
            previous_id = cards[current_i-1].id
            next_id = None
        
        elif card_id != first_id: # card in the middle
            previous_id = cards[current_i-1].id
            next_id = cards[current_i+1].id

    except Card.DoesNotExist:
        return redirect('create_card')
        #raise Http404("Question does not exist")

    return render(request, 'card_detail.html',
    {'card': card, 'num_of_cards':num_cards,
    'previous_id': previous_id, 'next_id': next_id,
    'start_of_cards': start_of_cards, 'end_of_cards': end_of_cards,})

# form to add new flashcards
class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    fields = ["question", "answer",] # fields for the form

    # after form successfully completed, return to creating more cards
    success_url = reverse_lazy("create_card") 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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

    def get_context_data(self, **kwargs): 
        'add additional context variables to the template context'
        context = super().get_context_data(**kwargs) # get the default context data from the parent class

        # get the id of current editing card
        context['current_id'] = self.object.pk
        return context

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

    # after finish review
    if request.method == 'POST':
        review_id = request.POST.get('review_id','')
        review = Review.objects.get(pk=review_id)
        
        # Get the current time
        now = timezone.now()
        # set the time of completion
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
        # is NOT completed, order by earliest date, get first queue
        earliest_scheduled_review = Review.objects.filter(completed__isnull=True).order_by('scheduled').first()
        flashcard = earliest_scheduled_review.flashcard
        
        # set the start time 
        earliest_scheduled_review.started = timezone.now()
        earliest_scheduled_review.save()
        
        # Render the review template, passing in the flashcards to review
        return render(request, 'review.html', {'card': flashcard, 'review': earliest_scheduled_review})
