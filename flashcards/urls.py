from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('text-file/', views.display_text_file, name='display_text_file'),
    path('cards/', views.display_cards, name='display_cards'),
    path('flashcard/<int:card_id>/', views.card_detail, name='detail'),
    # ex: /polls/5/results/
    # defines a URL pattern that maps the /text-file/ URL to the display_text_file view function.
]
# 'name' can be used later to refer specific views/