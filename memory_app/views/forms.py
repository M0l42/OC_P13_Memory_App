from memory_app.models import Cards, Deck, CardsState, QuickDeck, Category
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def create_desk_view(request):
    template_name = 'memory_app/create_desk_form.html'
    context = dict()
    context['title'] = 'Création de Deck'
    context['category'] = Category.objects.all()

    if request.POST:
        quick_mode = False
        private = False

        name = request.POST.get('title')
        category = Category.objects.get(pk=request.POST.get('category'))
        if request.POST.get('private'):
            private = True
        if request.POST.get('quickmode'):
            quick_mode = True
        user = request.user

        if quick_mode:
            deck = QuickDeck.objects.create(name=name, user=user, category=category, private=private)
        else:
            deck = Deck.objects.create(name=name, user=user, category=category, private=private)

        recto = request.POST.getlist('recto')
        verso = request.POST.getlist('verso')

        for i in range(len(recto)):
            card = Cards.objects.create(recto=recto[i], verso=verso[i])
            deck.cards.add(card)
            CardsState.objects.create(deck=deck, cards=card, rank=1, side=True)

        return redirect('deck_menu')
    return render(request, template_name, context=context)
