from django.contrib import admin
from .models import Cards, Deck, CardsState, QuickModeDeck, Category


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ('recto', 'verso')
    search_fields = ('recto', 'verso')


@admin.register(CardsState)
class CardsStateAdmin(admin.ModelAdmin):
    list_display = ('cards', 'deck', 'rank', 'date')
    search_fields = ('rank', )


@admin.register(Deck)
class DeskAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'favorite', 'category')
    search_fields = ('user', )


@admin.register(QuickModeDeck)
class QuickModeDeskAdmin(admin.ModelAdmin):
    list_display = ('deck', 'rank')
    search_fields = ('rank', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )
