from memory_app.models import Cards, CardsState, Deck, QuickModeDeck, Category
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import date, timedelta


def card_available(deck):
    today = date.today()
    available = False
    new_card = None
    for card in CardsState.objects.filter(deck=deck):
        if card.rank == 1:
            if card.date != today or card.new is True:
                new_card = card
                available = True
                break
        if card.rank == 2:
            if card.date == today - timedelta(days=2):
                new_card = card
                available = True
                break
        if card.rank == 3:
            if today.weekday() == 0:
                new_card = card
                available = True
                break
        if card.rank == 4:
            if today.day == 1:
                new_card = card
                available = True
                break
        if card.rank == 5:
            if today >= deck.created_at.replace(month=deck.created_at.month + 3):
                new_card = card
                available = True
                break
        if card.rank == 6:
            if today >= deck.created_at.replace(month=deck.created_at.month + 6):
                new_card = card
                available = True
                break
        if card.rank == 7:
            if today >= deck.created_at.replace(year=deck.created_at.year + 1):
                new_card = card
                available = True
                break
    return new_card, available


def deck_copy(deck_id, user):
    deck = Deck.objects.get(pk=deck_id)
    copied_deck = Deck.objects.create(user=user, name=deck.name, category=deck.category)
    quick = False
    try:
        QuickModeDeck.objects.get(deck=deck)
        QuickModeDeck.objects.create(deck=copied_deck)
        quick = True
    except ObjectDoesNotExist:
        pass

    for card in deck.cards.all():
        copied_deck.cards.add(card)
        CardsState.objects.create(deck=copied_deck, cards=card, rank=1, side=True)
    return quick


def deck_menu_view(requests):
    template_name = 'memory_app/deck_menu.html'
    context = dict()
    context['title'] = 'Normal Desk'
    context['deck'] = []
    context['quick_deck'] = []

    if requests.POST:
        deck_copy(requests.POST.get("copy"), requests.user)

    for deck in Deck.objects.filter(user=requests.user):
        try:
            QuickModeDeck.objects.get(deck=deck)
            context['quick_deck'].append(deck)
        except ObjectDoesNotExist:
            context['deck'].append(deck)
            card_available(deck)

    return render(requests, template_name, context=context)


def deck_update(requests, *args, **kwargs):
    template_name = 'memory_app/update_deck.html'
    context = dict()
    context['title'] = 'Normal Desk'
    deck = Deck.objects.get(pk=kwargs['deck'], user=requests.user)
    context['deck_name'] = deck.name
    context['deck'] = deck.cards.all()
    recto = requests.POST.getlist('recto')
    verso = requests.POST.getlist('verso')
    for i in range(len(recto)):
        card = Cards.objects.create(recto=recto[i], verso=verso[i])
        deck.cards.add(card)
        CardsState.objects.create(deck=deck, cards=card, rank=1, side=True)

    return render(requests, template_name, context=context)


class CheckMemoryView(View, LoginRequiredMixin):
    template_name = 'memory_app/memory.html'

    def init_deck(self, **kwargs):
        pass

    def update_card(self, data, context):
        try:
            card = data['state_cards'].cards
            context['deck'] = data['deck'].name
            if data['state_cards'].side:
                context['recto'] = card.recto
                context['verso'] = card.verso
            else:
                context['recto'] = card.verso
                context['verso'] = card.recto
        except IndexError:
            context['error'] = "No more cards"
            print("error")
        return context

    def get(self, request, *args, **kwargs):
        context = dict()
        data = self.init_deck(**kwargs)
        context = self.update_card(data, context)
        print(context)

        if request.is_ajax():
            if request.GET.get('next'):
                return JsonResponse(context, status=200)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pass


class QuickModeView(CheckMemoryView):
    template_name = 'memory_app/memory.html'

    def init_deck(self, **kwargs):
        data = dict()
        data['deck'] = Deck.objects.get(pk=kwargs['deck'], user=self.request.user)
        quick_mode = QuickModeDeck.objects.get(deck=data['deck'])
        try:
            data['state_cards'] = CardsState.objects.filter(deck=data['deck'], rank=quick_mode.rank)[0]
        except IndexError:
            if quick_mode.rank < 6:
                quick_mode.rank += 1
            else:
                quick_mode.rank = 1
                for state in CardsState.objects.filter(deck=data['deck'], rank=7):
                    state.rank = 5
                    state.save()
            quick_mode.save()
            data['state_cards'] = CardsState.objects.filter(deck=data['deck'], rank=quick_mode.rank)[0]
        data['quick_mode'] = quick_mode
        return data

    def post(self, request, *args, **kwargs):
        data = self.init_deck(**kwargs)
        state = data['state_cards'][0]
        if state.side:
            checking_side = state.cards.verso
        else:
            checking_side = state.cards.recto
        answer = request.POST.get('form_text')
        context = dict()
        if str(answer).lower() in str(checking_side).lower():
            print('wesh')
            if data['quick_mode'].rank == 4 or data['quick_mode'].rank == 6:
                state.rank += 1
            else:
                state.rank += 2
                print(state.rank)
            context['success'] = 200
        else:
            if data['quick_mode'].rank == 6:
                state.rank = 1
            else:
                state.rank += 1
            context['success'] = 400
        state.side = not state.side
        state.save()
        return JsonResponse(context, status=200)


class MemoryView(CheckMemoryView):
    template_name = 'memory_app/memory.html'

    def init_deck(self, **kwargs):
        data = dict()
        data['deck'] = Deck.objects.get(pk=kwargs['deck'], user=self.request.user)
        data['state_cards'] = []
        today = date.today()
        for card in CardsState.objects.filter(deck=data['deck']):
            if card.rank == 1:
                if card.date != today or card.new is True:
                    data['state_cards'].append(card)
            if card.rank == 2:
                if card.date == today - timedelta(days=2):
                    data['state_cards'].append(card)
            if card.rank == 3:
                if today.weekday() == 0:
                    data['state_cards'].append(card)
            if card.rank == 4:
                if today.day == 1:
                    data['state_cards'].append(card)
            if card.rank == 5:
                if today >= data['deck'].created_at.replace(month=data['deck'].created_at.month+3):
                    data['state_cards'].append(card)
            if card.rank == 6:
                if today >= data['deck'].created_at.replace(month=data['deck'].created_at.month+6):
                    data['state_cards'].append(card)
            if card.rank == 7:
                if today >= data['deck'].created_at.replace(year=data['deck'].created_at.year+1):
                    data['state_cards'].append(card)
        data['state_cards'] = data['state_cards'][0]
        return data

    def post(self, request, *args, **kwargs):
        data = self.init_deck(**kwargs)
        state = data['state_cards'][0]

        if state.side:
            checking_side = state.cards.verso
        else:
            checking_side = state.cards.recto

        answer = request.POST.get('form_text')
        context = dict()

        if str(answer).lower() in str(checking_side).lower():
            print('wesh')
            if state.rank < 7:
                state.rank += 1
            context['success'] = 200
        else:
            if state.rank != 1:
                state.rank -= 1
            context['success'] = 400
        if state.new:
            state.new = False
        state.side = not state.side
        state.save()
        return JsonResponse(context, status=200)


def deck_search_view(requests, *args, **kwargs):
    template_name = 'memory_app/deck_search.html'
    context = dict()
    context['title'] = 'Normal Desk'
    context['deck'] = []
    context['quick_deck'] = []
    context['categories'] = Category.objects.all()

    if requests.POST:
        deck_copy(requests.POST.get("copy"), requests.user)

    public_decks = Deck.objects.filter(private=False)
    try:
        category = Category.objects.get(slug=kwargs['slug'])
        public_decks = public_decks.filter(category=category)
    except KeyError:
        pass
    if requests.GET:
        public_decks = public_decks.filter(name__contains=requests.GET['query'])

    for deck in public_decks:
        try:
            QuickModeDeck.objects.get(deck=deck)
            context['quick_deck'].append(deck)
        except ObjectDoesNotExist:
            context['deck'].append(deck)
            card_available(deck)

    return render(requests, template_name, context=context)
