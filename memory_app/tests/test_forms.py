from django.test import TestCase
from django.urls import reverse
from memory_app.models import Cards, CardsState, Deck, Category
from . import create_testing_user


class DeckCreationTestCase(TestCase):
    def setUp(self):
        create_testing_user()
        category = Category.objects.create(name="test", slug="test")
        self.form = {
            "title": "test",
            "category": category.id,
            "private": False,
        }

    def test_deck_creation_page_return_302(self):
        response = self.client.get(reverse('create_desk'))
        self.assertEqual(response.status_code, 302)

    def test_create_desk(self):
        user = self.client.login(username='testuser', password='12345')
        old_deck = Deck.objects.filter(user=user).count()
        self.client.post(reverse('create_desk'), self.form)
        new_deck = Deck.objects.all().count()
        self.assertEqual(new_deck, old_deck + 1)

    def test_add_cards(self):
        self.form['recto'] = ['aaaa', 'cccc']
        self.form['verso'] = ['aaaa', 'cccc']
        self.client.login(username='testuser', password='12345')

        old_cards_count = Cards.objects.all().count()
        old_cards_state_count = CardsState.objects.all().count()

        self.client.post(reverse('create_desk'), self.form)

        new_cards_count = Cards.objects.all().count()
        new_cards_state_count = CardsState.objects.all().count()

        self.assertEqual(new_cards_count, old_cards_count + 2)
        self.assertEqual(new_cards_state_count, old_cards_state_count + 2)

    def test_add_empty_cards(self):
        self.form['recto'] = ['']
        self.form['verso'] = ['']
        self.client.login(username='testuser', password='12345')

        old_cards_count = Cards.objects.all().count()
        old_cards_state_count = CardsState.objects.all().count()

        self.client.post(reverse('create_desk'), self.form)

        new_cards_count = Cards.objects.all().count()
        new_cards_state_count = CardsState.objects.all().count()

        self.assertEqual(new_cards_count, old_cards_count)
        self.assertEqual(new_cards_state_count, old_cards_state_count)
