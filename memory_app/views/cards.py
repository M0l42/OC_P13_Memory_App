from memory_app.models import Cards, CardsState, Deck, QuickDeck, Category, DeckImage
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import os


def deck_copy(deck_id, user):
    deck = Deck.objects.get(pk=deck_id)

    quick = False
    try:
        QuickDeck.objects.get(pk=deck)
        copied_deck = QuickDeck.objects.create(user=user, name=deck.name, category=deck.category)
        quick = True
    except ObjectDoesNotExist:
        copied_deck = Deck.objects.create(user=user, name=deck.name, category=deck.category)

    for card in deck.cards.all():
        copied_deck.cards.add(card)
        CardsState.objects.create(deck=copied_deck, cards=card, rank=1, side=True)
    return quick


@login_required
def deck_menu_view(requests):
    template_name = 'memory_app/deck_menu.html'
    context = dict()
    context['title'] = 'Menu'
    context['deck'] = []
    context['quick_deck'] = []

    if requests.POST:
        id = requests.POST.get("delete")
        try:
            deck = QuickDeck.objects.get(pk=id, user=requests.user)
        except ObjectDoesNotExist:
            deck = Deck.objects.get(pk=id, user=requests.user)
        deck.delete()

    for deck in Deck.objects.filter(user=requests.user).order_by('favorite'):
        try:
            context['quick_deck'].append(QuickDeck.objects.get(pk=deck))
        except ObjectDoesNotExist:
            context['deck'].append(deck)

    return render(requests, template_name, context=context)


@login_required
def deck_update(requests, *args, **kwargs):
    template_name = 'memory_app/update_deck.html'
    context = dict()
    context['title'] = 'Update'
    deck = Deck.objects.get(pk=kwargs['deck'], user=requests.user)
    context['deck_name'] = deck.name
    context['deck'] = deck.cards.all()
    if requests.POST:
        if requests.POST.getlist('favorite'):
            deck.favorite = True
            deck.save()
        recto = requests.POST.getlist('recto')
        verso = requests.POST.getlist('verso')
        for i in range(len(recto)):
            card = Cards.objects.create(recto=recto[i], verso=verso[i])
            deck.cards.add(card)
            CardsState.objects.create(deck=deck, cards=card, rank=1, side=True)

    return render(requests, template_name, context=context)


class CheckMemoryView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'memory_app/memory.html'

    def get(self, request, *args, **kwargs):
        try:
            deck = QuickDeck.objects.get(pk=kwargs['deck'], user=self.request.user)
        except ObjectDoesNotExist:
            deck = Deck.objects.get(pk=kwargs['deck'], user=self.request.user)
        context = deck.update()
        context['title'] = 'Révision'

        if request.is_ajax():
            if request.GET.get('next'):
                context['deck'] = None
                return JsonResponse(context, status=200)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pass


class QuickModeView(CheckMemoryView):
    template_name = 'memory_app/memory.html'

    def post(self, request, *args, **kwargs):
        deck = QuickDeck.objects.get(pk=kwargs['deck'], user=self.request.user)
        state = deck.get_card()
        context = dict()

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
            if deck.rank == 4 or deck.rank == 6:
                state.rank += 1
            else:
                state.rank += 2
            context['success'] = 200
        else:
            if deck.rank == 6:
                state.rank = 1
            else:
                state.rank += 1
            context['success'] = 400
        state.side = not state.side
        state.save()
        return JsonResponse(context, status=200)


class MemoryView(CheckMemoryView):
    template_name = 'memory_app/memory.html'

    def post(self, request, *args, **kwargs):
        deck = Deck.objects.get(pk=kwargs['deck'], user=self.request.user)
        card = deck.get_card()
        context = dict()

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
            if card.rank < 7:
                card.rank += 1
            context['success'] = 200
        else:
            if card.rank != 1:
                card.rank -= 1
            context['success'] = 400
        if card.new:
            card.new = False
        card.side = not card.side
        card.save()
        return JsonResponse(context, status=200)


@login_required
def deck_search_view(requests, *args, **kwargs):
    template_name = 'memory_app/deck_search.html'
    context = dict()
    context['title'] = 'Recherche'
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
            context['quick_deck'].append(QuickDeck.objects.get(pk=deck))
        except ObjectDoesNotExist:
            context['deck'].append(deck)

    return render(requests, template_name, context=context)


@login_required
def customize_deck(requests, *args, **kwargs):
    template_name = 'memory_app/customize_deck.html'
    context = dict()
    context['title'] = 'Personnalisation'
    try:
        context['deck'] = QuickDeck.objects.get(pk=kwargs['deck'])
    except ObjectDoesNotExist:
        context['deck'] = Deck.objects.get(pk=kwargs['deck'])
    context['image'] = DeckImage.objects.all()

    if requests.GET:
        if requests.is_ajax():
            data = dict()
            try:
                image = DeckImage.objects.get(pk=requests.GET.get('image'))
                data['image'] = os.path.basename(image.image.name)
            except ValueError:
                pass
        return JsonResponse(data, status=200)

    if requests.POST:
        try:
            deck = QuickDeck.objects.get(pk=kwargs['deck'])
        except ObjectDoesNotExist:
            deck = Deck.objects.get(pk=kwargs['deck'])

        color = requests.POST.get("color")
        image = requests.POST.get("image")

        if image != 'None':
            deck.image = DeckImage.objects.get(pk=image)
        elif color:
            deck.color = color
            deck.image = None

        deck.color_text = requests.POST.get("color_text")

        deck.save()
        return redirect('deck_menu')

    return render(requests, template_name, context=context)
