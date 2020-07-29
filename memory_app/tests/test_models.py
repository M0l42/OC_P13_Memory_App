from django.test import TestCase
from memory_app.models import Cards, CardsState, Deck, QuickDeck, Category, DeckImage
from . import create_testing_user, create_deck

from freezegun import freeze_time
from datetime import date, timedelta


class DeckTestCase(TestCase):
    @freeze_time("2020-07-25")
    def setUp(self):
        # user = create_testing_user()
        # category = Category.objects.create(name="test", slug="test")
        # self.deck = Deck.objects.create(name="test", user=user, category=category)
        # self.card = Cards.objects.create(recto="aaaa", verso="bbbb")
        # self.deck.cards.add(self.card)
        self.deck, self.state = create_deck()
        # self.card = state.cards

    @freeze_time(date.today() - timedelta(days=2))
    def create_card_two_days_ago(self):
        self.state.rank = 2
        self.state.save()

    @freeze_time("2020-07-25")
    def create_card_right_time(self, rank):
        self.state.rank = rank
        self.state.save()

    def test_get_card_rank_1_success(self):
        self.assertEqual(self.deck.get_card(), self.state)

    def test_get_card_rank_1_failure(self):
        self.state.new = False
        self.state.save()
        self.assertNotEqual(self.deck.get_card(), self.state)

    def test_get_card_rank_2_success(self):
        self.create_card_two_days_ago()
        self.assertEqual(self.deck.get_card(), self.state)

    def test_get_card_rank_2_failure(self):
        self.state.rank = 2
        self.state.save()
        self.assertNotEqual(self.deck.get_card(), self.state)

    @freeze_time("2020-07-20")
    def test_get_card_rank_3_success(self):
        self.state.rank = 3
        self.state.save()
        self.assertEqual(self.deck.get_card(), self.state)

    @freeze_time("2020-07-21")
    def test_get_card_rank_3_failure(self):
        self.state.rank = 3
        self.state.save()
        self.assertNotEqual(self.deck.get_card(), self.state)

    @freeze_time("2020-07-01")
    def test_get_card_rank_4_success(self):
        self.state.rank = 4
        self.state.save()
        self.assertEqual(self.deck.get_card(), self.state)

    @freeze_time("2020-07-02")
    def test_get_card_rank_4_failure(self):
        self.state.rank = 4
        self.state.save()
        self.assertNotEqual(self.deck.get_card(), self.state)

    @freeze_time("2020-10-25")
    def test_get_card_rank_5_success(self):
        self.create_card_right_time(5)
        self.assertEqual(self.deck.get_card(), self.state)

    @freeze_time("2020-08-25")
    def test_get_card_rank_5_failure(self):
        self.state.rank = 5
        self.state.save()
        self.assertNotEqual(self.deck.get_card(), self.state)

    @freeze_time("2021-01-25")
    def test_get_card_rank_6_success(self):
        self.create_card_right_time(6)
        self.assertEqual(self.deck.get_card(), self.state)

    @freeze_time("2020-12-25")
    def test_get_card_rank_6_failure(self):
        self.state.rank = 6
        self.state.save()
        self.assertNotEqual(self.deck.get_card(), self.state)

    @freeze_time("2021-07-25")
    def test_get_card_rank_7_success(self):
        self.create_card_right_time(7)
        self.assertEqual(self.deck.get_card(), self.state)

    @freeze_time("2021-06-25")
    def test_get_card_rank_7_failure(self):
        self.state.rank = 7
        self.state.save()
        self.assertNotEqual(self.deck.get_card(), self.state)

    def test_update_card_side_recto(self):
        context = self.deck.update()
        self.assertEqual(context['recto'], self.state.cards.recto)
        self.assertEqual(context['verso'], self.state.cards.verso)

    def test_update_card_side_verso(self):
        self.state.side = False
        self.state.save()
        context = self.deck.update()
        self.assertEqual(context['recto'], self.state.cards.verso)
        self.assertEqual(context['verso'], self.state.cards.recto)

    @freeze_time("2020-07-25")
    def test_update_error(self):
        self.state.new = False
        self.state.save()
        context = self.deck.update()
        self.assertEqual(context['error'], "No more cards")


class QuickDeckTestCase(TestCase):
    def setUp(self):
        self.deck, self.state = create_deck(quick=True)

    def test_deck_and_card_rank_1(self):
        self.state.rank = 1
        self.state.save()
        self.assertEqual(self.deck.get_card(), self.state)

    def test_deck_rank_1_and_card_rank_3(self):
        self.state.rank = 3
        self.state.save()
        self.assertEqual(self.deck.get_card(), self.state)
        self.assertEqual(self.deck.rank, 3)

    def test_deck_rank_3_and_card_rank_1(self):
        self.deck.rank = 3
        self.deck.save()
        self.state.rank = 1
        self.state.save()
        self.assertEqual(self.deck.get_card(), self.state)
        self.assertEqual(self.deck.rank, 1)

    def test_card_rank_7(self):
        self.state.rank = 7
        self.state.save()
        self.assertEqual(self.deck.get_card().rank, 5)
