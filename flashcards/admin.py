from django.contrib import admin
from .models import Card

# register the flashcard model with the admin site
# creates an admin interface for the 'Card' model: for add, edit, delete
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from .models import Card

#creates admin interface for the 'Card' model: add, edit, delete
class CardAdmin(admin.ModelAdmin):
    pass
