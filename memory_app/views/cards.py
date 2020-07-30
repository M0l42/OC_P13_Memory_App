from memory_app.models import Cards, CardsState, Deck, QuickDeck, Category, DeckImage
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import os


def deck_copy(deck_id, user):
    """
    Get infos of a deck and create a new one with it

    :param deck_id:
    :param user:
    :return:
        A boolean to tell of the new deck is a QuickDeck
    """
    deck = Deck.objects.get(pk=deck_id)

    quick = False
    try:
        QuickDeck.objects.get(pk=deck)
        copied_deck = QuickDeck.objects.create(user=user, name=deck.name, category=deck.category)
        quick = True
    except ObjectDoesNotExist:
        copied_deck = Deck.objects.create(user=user, name=deck.name, category=deck.category)
    copied_deck.image = deck.image
    copied_deck.color = deck.color
    copied_deck.color_text = deck.color_text
    copied_deck.save()

    for card in deck.cards.all():
        # Add all deck's cards to the new deck
        copied_deck.cards.add(card)
        CardsState.objects.create(deck=copied_deck, cards=card, rank=1, side=True)
    return quick


def get_deck(user, id_deck):
    """
    Get the right form of Deck

    :param user:
    :param id_deck:
    :return:
        deck
    """
    try:
        deck = QuickDeck.objects.get(pk=id_deck, user=user)
    except ObjectDoesNotExist:
        deck = Deck.objects.get(pk=id_deck, user=user)
    return deck


def sort_deck(context, pack_of_deck, available=None):
    """
    Sort the deck on two list : quick_deck and deck inside the given context

    :param context:
    :param pack_of_deck:
    :param available:
    """

    context['deck'] = []
    context['unavailable_deck'] = []
    context['quick_deck'] = []
    context['unavailable_quick_deck'] = []
    for deck in pack_of_deck:
        try:
            quick_deck = QuickDeck.objects.get(pk=deck)
            if available:
                if quick_deck.get_card():
                    context['quick_deck'].append(quick_deck)
                else:
                    context['unavailable_quick_deck'].append(quick_deck)
            else:
                context['quick_deck'].append(quick_deck)
        except ObjectDoesNotExist:
            if available:
                if deck.get_card():
                    context['deck'].append(deck)
                else:
                    context['unavailable_deck'].append(deck)
            else:
                context['deck'].append(deck)


def create_multiple_cards(deck, requests):
    # get cards
    recto = requests.POST.getlist('recto')
    verso = requests.POST.getlist('verso')

    for i in range(len(recto)):
        if recto[i]:
            card = Cards.objects.create(recto=recto[i], verso=verso[i])
            deck.cards.add(card)
            CardsState.objects.create(deck=deck, cards=card, rank=1, side=True)


@login_required
def deck_menu_view(requests):
    """
    View of the deck's menu.
    Show all the Deck and the QuickDeck of the user.
    The Deck on Favorite will be shown at first.
    :param requests:
    :return:
        A rendered page.
    """
    template_name = 'memory_app/deck_menu.html'
    context = dict()
    context['title'] = 'Menu'

    if requests.POST:
        # Delete a choosen deck.
        id = requests.POST.get("delete")
        deck = get_deck(requests.user, id)
        deck.delete()

    sort_deck(context, Deck.objects.filter(user=requests.user).order_by('favorite'), available=True)

    return render(requests, template_name, context=context)


@login_required
def deck_update(requests, *args, **kwargs):
    """
    Update a choosen Deck.
    Add new Cards and update some infos of the Deck

    :param requests:
    :param args:
    :param kwargs:
    :return:
        A rendered page
    """
    template_name = 'memory_app/update_deck.html'
    context = dict()
    context['title'] = 'Update'
    deck = Deck.objects.get(pk=kwargs['deck'], user=requests.user)
    context['deck_name'] = deck.name
    context['deck'] = deck.cards.all()

    if requests.POST:
        if requests.POST.get('favorite'):
            deck.favorite = True
            deck.save()

        if requests.POST.get('private'):
            deck.private = True
            deck.save()

        if requests.POST.get('title'):
            deck.name = requests.POST.get('title')
            deck.save()
        create_multiple_cards(deck, requests)
        return redirect('deck_menu')

    return render(requests, template_name, context=context)


@login_required
def show_deck_view(requests, *args, **kwargs):
    """
    A Basic page to show all cards of a Deck

    :param requests:
    :param args:
    :param kwargs:
    :return:
        A rendered page
    """
    template_name = 'memory_app/show_deck.html'
    context = dict()
    context['title'] = 'Update'
    deck = Deck.objects.get(pk=kwargs['deck'])
    context['deck_name'] = deck.name
    context['deck'] = deck.cards.all()

    return render(requests, template_name, context=context)


class CheckMemoryView(LoginRequiredMixin, View):
    """
    A class of LoginRequiredMixin and View for user to do some revision of their flashcards

    ...

    Attributes
    ----------
    login_url : str
        The url of the login page
    redirect_field_name : str
        what to do
    template_name : str
        the name of the template

    Methods
    -------
    get:
        Get the context of the view
    post:
        Change all the info the users filled

    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'memory_app/memory.html'

    def get(self, *args, **kwargs):
        """
        Get the Cards to show to the user.

        :param request:
        :param args:
        :param kwargs:
        :return:
            A rendered page or A JsonResponse
        """

        deck = get_deck(self.request.user, kwargs['deck'])
        context = deck.update()
        context['title'] = 'Révision'

        if self.request.is_ajax():
            if self.request.GET.get('next'):
                context['deck'] = None
                return JsonResponse(context, status=200)
        return render(self.request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pass


class QuickModeView(CheckMemoryView):
    """
    Child class of CheckMemoryView,
    Will handle the cards for a QuickDeck
    """

    def post(self, request, *args, **kwargs):
        """
        Will receive data from a post-text form
        with the answer of the user of the other side of the card

        :param request:
        :param args:
        :param kwargs:
        :return:
            A JsonResponse with all the data needed
        """

        deck = QuickDeck.objects.get(pk=kwargs['deck'], user=self.request.user)
        state = deck.get_card()
        context = dict()

        # To Check the right side and show the right one to the user
        if state.side:
            checking_side = state.cards.verso
            context['recto'] = state.cards.recto
            context['verso'] = state.cards.verso
        else:
            checking_side = state.cards.recto
            context['verso'] = state.cards.recto
            context['recto'] = state.cards.verso

        answer = request.POST.get('form_text')
        if str(answer).lower() == str(checking_side).lower():
            # We want all cards to be on Rank 5 when the deck are on rank 4
            # There's only 7 rank so we need to be sure we don't overlaps
            if deck.rank == 4 or deck.rank == 6:
                state.rank += 1
            else:
                state.rank += 2
            context['success'] = 200
        else:
            if deck.rank == 6:
                # Go back to rank one if the user get it wrong
                state.rank = 1
            else:
                state.rank += 1
            context['success'] = 400
        # Make sure to switch side.
        state.side = not state.side
        state.save()

        return JsonResponse(context, status=200)


class MemoryView(CheckMemoryView):
    """
    Child class of CheckMemoryView,
    Will handle the cards for a Deck
    """

    def post(self, request, *args, **kwargs):
        """
        Will receive data from a post-text form
        with the answer of the user of the other side of the card

        :param request:
        :param args:
        :param kwargs:
        :return:
            A JsonResponse with all the data needed
        """

        deck = Deck.objects.get(pk=kwargs['deck'], user=self.request.user)
        card = deck.get_card()
        context = dict()

        # To Check the right side and show the right one to the user
        if card.side:
            checking_side = card.cards.verso
            context['recto'] = card.cards.recto
            context['verso'] = card.cards.verso
        else:
            checking_side = card.cards.recto
            context['verso'] = card.cards.recto
            context['recto'] = card.cards.verso

        answer = request.POST.get('form_text')

        if str(answer).lower() == str(checking_side).lower():
            # All succeded Cards go to the next rank except for the 7th
            if card.rank < 7:
                card.rank += 1
            context['success'] = 200
        else:
            # All Failed Cards go the the previous rank except for the 1st rank
            if card.rank != 1:
                card.rank -= 1
            context['success'] = 400
        if card.new:
            # To be able to check the cards who's been created the same day
            card.new = False
        # Make sure to switch side.
        card.side = not card.side
        card.save()

        return JsonResponse(context, status=200)


@login_required
def deck_search_view(requests, *args, **kwargs):
    """
    Show every public Deck
    Can be filter by Category or query or both

    :param requests:
    :param args:
    :param kwargs:
    :return:
        A rendered page
    """
    template_name = 'memory_app/deck_search.html'
    context = dict()
    context['title'] = 'Recherche'
    context['categories'] = Category.objects.all()

    if requests.POST:
        deck_copy(requests.POST.get("copy"), requests.user)

    public_decks = Deck.objects.filter(private=False)

    try:
        # Filter by category if the user selected one
        category = Category.objects.get(slug=kwargs['slug'])
        public_decks = public_decks.filter(category=category)
    except KeyError:
        pass

    if requests.GET:
        # Filter by query if the send one
        public_decks = public_decks.filter(name__contains=requests.GET['query'])

    sort_deck(context, public_decks)

    return render(requests, template_name, context=context)


@login_required
def customize_deck(requests, *args, **kwargs):
    """
    Handle custimisation of a Deck
    Add Image or color to it.

    :param requests:
    :param args:
    :param kwargs:
    :return:
        A rendered page or a JsonResponse or a Redirect
    """

    template_name = 'memory_app/customize_deck.html'
    context = dict()
    context['title'] = 'Personnalisation'

    deck = get_deck(requests.user, kwargs['deck'])
    context['deck'] = deck

    context['image'] = DeckImage.objects.all()

    if requests.GET:
        if requests.is_ajax():
            # To show choosen image to the user.
            data = dict()
            try:
                image = DeckImage.objects.get(pk=requests.GET.get('image'))
                print(image.image.url)
                data['image'] = os.path.basename(image.image.name)
            except ValueError:
                pass
            return JsonResponse(data, status=200)

    if requests.POST:
        # To save changes of the deck infos
        color = requests.POST.get("color")
        image = requests.POST.get("image")

        if image != 'None':
            deck.image = DeckImage.objects.get(pk=image)
        elif color:
            # If a color has been selected, delete the image
            deck.color = color
            deck.image = None

        deck.color_text = requests.POST.get("color_text")

        deck.save()
        return redirect('deck_menu')

    return render(requests, template_name, context=context)



