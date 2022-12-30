from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('text-file/', views.display_text_file, name='display_text_file'),
    path('cards/', views.display_cards, name='display_cards'),
    path('flashcard/<int:card_id>/', views.card_detail, name='display_card'),
    path("flashcard/new",views.CardCreateView.as_view(),name="create_card"),
    # will look for card_form.html template by default
   
]
# 'name' can be used later to refer specific views