from django.contrib import admin
from .models import Cards, Desk, CardsState


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ('recto', 'verso')
    search_fields = ('recto', 'verso')


@admin.register(CardsState)
class CardsStateAdmin(admin.ModelAdmin):
    list_display = ('cards', 'desk', 'rank')
    search_fields = ('rank', )


@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('user', )
