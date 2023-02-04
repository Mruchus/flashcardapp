from django.urls import path
from . import views

urlpatterns = [
    # test urls
    path('hello/', views.hello, name='hello'),
    path('text-file/', views.display_text_file, name='display_text_file'),

    # home page
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),

    # card views
    path('cards/', views.display_cards, name='display_cards'),
    # view individual cards
    path('flashcard/<int:card_id>/', views.card_detail, name='display_card'),

    # dynamic views
    # will look for card_form.html template by default
    path("flashcard/new",views.CardCreateView.as_view(),name="create_card"), 
    path("edit/<int:pk>",views.CardUpdateView.as_view(),name="card_update"),
    path("delete/<int:pk>",views.CardDeleteView.as_view(),name="card_delete"),

    # review page - start review
    path("review/",views.review,name="review"), 

    path("logout", views.logout_view, name="logout")    

]
# 'name' can be used later to refer specific views