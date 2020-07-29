from memory_app.models import Deck, QuickDeck, Category
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .cards import create_multiple_cards


@login_required
def create_deck_view(request):
    """
    A form view function to create new deck

    :param request:
    :return:
        rendered page or a redirect to the menu
    """

    template_name = 'memory_app/create_desk_form.html'
    context = dict()
    context['title'] = 'Création de Deck'
    context['category'] = Category.objects.all()

    if request.POST:
        quick_mode = False
        private = False

        # get infos
        name = request.POST.get('title')
        category = Category.objects.get(pk=request.POST.get('category'))
        if request.POST.get('private'):
            private = True
        if request.POST.get('quickmode'):
            quick_mode = True
        user = request.user

        # create new deck
        if quick_mode:
            deck = QuickDeck.objects.create(name=name, user=user, category=category, private=private)
        else:
            deck = Deck.objects.create(name=name, user=user, category=category, private=private)

        create_multiple_cards(deck, request)
        return redirect('deck_menu')
    return render(request, template_name, context=context)
