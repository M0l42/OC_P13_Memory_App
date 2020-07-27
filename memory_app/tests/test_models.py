from django.test import TestCase
from memory_app.models import Cards, CardsState, Deck, QuickDeck, Category, DeckImage
from . import create_testing_user

from freezegun import freeze_time
from datetime import date, timedelta


class DeckTestCase(TestCase):
    @freeze_time("2020-07-25")
    def setUp(self):
        user = create_testing_user()
        category = Category.objects.create(name="test", slug="test")
        self.deck = Deck.objects.create(name="test", user=user, category=category)
        self.card = Cards.objects.create(recto="aaaa", verso="bbbb")
        self.deck.cards.add(self.card)

    @freeze_time(date.today() - timedelta(days=2))
    def create_card_two_days_ago(self):
        return CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=2)

    def test_get_card_rank_1_success(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True)
        self.assertEqual(self.deck.get_card(), state)

    def test_get_card_rank_1_failure(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, new=False)
        self.assertNotEqual(self.deck.get_card(), state)

    def test_get_card_rank_2_success(self):
        state = self.create_card_two_days_ago()
        self.assertEqual(self.deck.get_card(), state)

    def test_get_card_rank_2_failure(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=2)
        self.assertNotEqual(self.deck.get_card(), state)

    @freeze_time("2020-07-20")
    def test_get_card_rank_3_success(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=3)
        self.assertEqual(self.deck.get_card(), state)

    @freeze_time("2020-07-21")
    def test_get_card_rank_3_failure(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=3)
        self.assertNotEqual(self.deck.get_card(), state)

    @freeze_time("2020-07-01")
    def test_get_card_rank_4_success(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=4)
        self.assertEqual(self.deck.get_card(), state)

    @freeze_time("2020-07-02")
    def test_get_card_rank_4_failure(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=4)
        self.assertNotEqual(self.deck.get_card(), state)

    @freeze_time("2020-12-25")
    def test_get_card_rank_5_success(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=5)
        self.assertEqual(self.deck.get_card(), state)

    @freeze_time("2020-08-25")
    def test_get_card_rank_5_failure(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=5)
        self.assertNotEqual(self.deck.get_card(), state)

    @freeze_time("2021-01-25")
    def test_get_card_rank_6_success(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=6)
        self.assertEqual(self.deck.get_card(), state)

    @freeze_time("2020-12-25")
    def test_get_card_rank_6_failure(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=6)
        self.assertNotEqual(self.deck.get_card(), state)

    @freeze_time("2021-07-25")
    def test_get_card_rank_7_success(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=7)
        self.assertEqual(self.deck.get_card(), state)

    @freeze_time("2021-06-25")
    def test_get_card_rank_7_failure(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=7)
        self.assertNotEqual(self.deck.get_card(), state)

    def test_update_card_side_recto(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=1)
        context = self.deck.update()
        self.assertEqual(context['recto'], state.cards.recto)
        self.assertEqual(context['verso'], state.cards.verso)

    def test_update_card_side_verso(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=False, rank=1)
        context = self.deck.update()
        self.assertEqual(context['recto'], state.cards.verso)
        self.assertEqual(context['verso'], state.cards.recto)

    @freeze_time("2020-07-25")
    def test_update_error(self):
        CardsState.objects.create(deck=self.deck, cards=self.card, side=False, rank=1, new=False)
        context = self.deck.update()
        self.assertEqual(context['error'], "No more cards")


class QuickDeckTestCase(TestCase):
    def setUp(self):
        user = create_testing_user()
        category = Category.objects.create(name="test", slug="test")
        self.deck = QuickDeck.objects.create(name="test", user=user, category=category)
        self.card = Cards.objects.create(recto="aaaa", verso="bbbb")
        self.deck.cards.add(self.card)

    def test_deck_and_card_rank_1(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=1)
        self.assertEqual(self.deck.get_card(), state)

    def test_deck_rank_1_and_card_rank_3(self):
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=3)
        self.assertEqual(self.deck.get_card(), state)
        self.assertEqual(self.deck.rank, 3)

    def test_deck_rank_3_and_card_rank_1(self):
        self.deck.rank = 3
        state = CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=1)
        self.assertEqual(self.deck.get_card(), state)
        self.assertEqual(self.deck.rank, 1)

    def test_card_rank_7(self):
        CardsState.objects.create(deck=self.deck, cards=self.card, side=True, rank=7)
        self.assertEqual(self.deck.get_card().rank, 5)
