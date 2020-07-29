from django.contrib.auth.models import User
from memory_app.models import Cards, CardsState, Deck, QuickDeck, Category, DeckImage


def create_testing_user(username='testuser', password='12345'):
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    return user


def create_deck(username='testuser', password='12345', name='test', recto='aaaa', verso='bbbb', quick=False):
    user = create_testing_user(username=username, password=password)
    category = Category.objects.create(name=name, slug=name)
    deck = Deck.objects.create(name=name, user=user, category=category)
    quick_deck = QuickDeck.objects.create(name="test", user=user, category=category)
    card = Cards.objects.create(recto=recto, verso=verso)
    if quick:
        quick_deck.cards.add(card)
        state = CardsState.objects.create(deck=quick_deck, cards=card, side=True)
        return quick_deck, state
    else:
        deck.cards.add(card)
        state = CardsState.objects.create(deck=deck, cards=card, side=True)
        return deck, state
