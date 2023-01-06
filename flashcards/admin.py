from django.contrib import admin
from .models import Card, Review

# register the flashcard model with the admin site
# creates an admin interface for the 'Card' model: for add, edit, delete
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
