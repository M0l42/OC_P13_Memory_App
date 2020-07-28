from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from memory_app.models import Cards, CardsState, Deck, QuickDeck, Category, DeckImage
from . import create_testing_user

import os
from freezegun import freeze_time


class DeckMenuTestCase(TestCase):
    def setUp(self):
        user = create_testing_user()
        category = Category.objects.create(name="test", slug="test")
        self.deck = Deck.objects.create(name="test", user=user, category=category)
        QuickDeck.objects.create(name="test", user=user, category=category)

    def test_deck_menu_page_return_302(self):
        response = self.client.get(reverse('deck_menu'))
        self.assertEqual(response.status_code, 302)

    def test_deck_menu_page_return_200(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('deck_menu'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['deck'], ['<Deck: test>'])
        self.assertQuerysetEqual(response.context['quick_deck'], ['<QuickDeck: test>'])

    def test_copy_deck(self):
        old_deck = Deck.objects.count()
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('deck_menu'), {'delete': self.deck.id})
        new_deck = Deck.objects.count()
        self.assertEqual(new_deck, old_deck - 1)


class DeckUpdateTestCase(TestCase):
    def setUp(self):
        user = create_testing_user()
        category = Category.objects.create(name="test", slug="test")
        self.deck = Deck.objects.create(name="test", user=user, category=category)
        card = Cards.objects.create(recto="aaaa", verso="bbbb")
        self.deck.cards.add(card)

    def test_deck_update_page_return_302(self):
        response = self.client.get(reverse('deck_update', args={self.deck.id}))
        self.assertEqual(response.status_code, 302)

    def test_deck_update_page_return_200(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('deck_update', args={self.deck.id}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['deck'], ['<Cards: aaaa - bbbb>'])

    def test_add_cards(self):
        old_card = self.deck.cards.count()
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('deck_update', args={self.deck.id}), {'recto': ["cccc"], 'verso': ["dddd"]})
        new_card = self.deck.cards.count()
        self.assertEqual(new_card, old_card + 1)


class DeckSearchTestCase(TestCase):
    def setUp(self):
        user = create_testing_user()
        other_user = create_testing_user(username='other user', password='12345')
        category = Category.objects.create(name="test", slug="test")
        other_category = Category.objects.create(name="aaaa", slug="aaaa")

        self.deck = Deck.objects.create(name="test", user=user, category=category)
        card = Cards.objects.create(recto="aaaa", verso="bbbb")
        self.deck.cards.add(card)
        QuickDeck.objects.create(name="test", user=user, category=category)

        self.other_deck = Deck.objects.create(name="aaaa", user=other_user, category=other_category)
        card = Cards.objects.create(recto="aaaa", verso="bbbb")
        self.other_deck.cards.add(card)
        QuickDeck.objects.create(name="test", user=other_user, category=other_category, private=True)

    def test_deck_update_page_return_302(self):
        response = self.client.get(reverse('deck_search'))
        self.assertEqual(response.status_code, 302)

    def test_deck_update_page_return_200(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('deck_search'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['deck'], ['<Deck: test>', '<Deck: aaaa>'])
        self.assertQuerysetEqual(response.context['quick_deck'], ['<QuickDeck: test>'])

    def test_copy_deck(self):
        old_deck = Deck.objects.count()
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('deck_search'), {'copy': self.other_deck.id})
        new_deck = Deck.objects.count()
        self.assertEqual(new_deck, old_deck + 1)


class CustomizeDeckTestCase(TestCase):
    def setUp(self):
        user = create_testing_user()
        category = Category.objects.create(name="test", slug="test")
        self.deck = Deck.objects.create(name="test", user=user, category=category)

        self.deck_image = DeckImage.objects.create(name="test image")
        path_file = os.path.join(os.getcwd(), "memory_app/tests/image_test.jpg")

        self.deck_image.image = SimpleUploadedFile(name='image_test.jpg', content=open(path_file, 'rb').read(),
                                                   content_type='image/jpeg')
        self.deck_image.save()

    def delete_image(self):
        path_dir_img = os.path.join(os.path.join(os.getcwd(), "memory_app/static/img/deck"))
        path_file = os.path.join(path_dir_img, "image_test.jpg")
        os.remove(path_file)

    def test_deck_update_page_return_302(self):
        response = self.client.get(reverse('customize-deck', args={self.deck.id}))
        self.assertEqual(response.status_code, 302)
        self.delete_image()

    def test_deck_update_page_return_200(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('customize-deck', args={self.deck.id}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['image'], ['<DeckImage: test image>'])
        self.delete_image()

    def test_set_image_deck(self):
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('customize-deck', args={self.deck.id}), {'image': self.deck_image.id})
        deck = Deck.objects.get(pk=self.deck.id)
        self.assertEqual(deck.image, self.deck_image)
        self.delete_image()

    def test_set_color_deck(self):
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('customize-deck', args={self.deck.id}), {'color': "#fefefe", 'color_text': "#ffffff",
                                                                          "image": "None"})
        deck = Deck.objects.get(pk=self.deck.id)
        self.assertEqual("#fefefe", deck.color)
        self.assertEqual("#ffffff", deck.color_text)
        self.delete_image()


class MemoryTestCase(TestCase):
    @freeze_time("2020-07-25")
    def setUp(self):
        user = create_testing_user()
        category = Category.objects.create(name="test", slug="test")

        self.deck = Deck.objects.create(name="test", user=user, category=category)
        card = Cards.objects.create(recto="aaaa", verso="bbbb")
        self.deck.cards.add(card)
        self.state = CardsState.objects.create(deck=self.deck, cards=card, side=True)

    def test_deck_update_page_return_302(self):
        response = self.client.get(reverse('memory', args={self.deck.id}))
        self.assertEqual(response.status_code, 302)

    def test_deck_update_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('memory', args={self.deck.id}))
        self.assertEqual(response.context['deck'], self.deck)
        self.assertEqual(response.context['recto'], 'aaaa')
        self.assertEqual(response.context['verso'], 'bbbb')

    def test_deck_post(self):
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('memory', args={self.deck.id}), {'form_text': "bbbb"})
        state = CardsState.objects.get(pk=self.state.id)
        self.assertNotEqual(state.side, self.state.side)
        self.assertEqual(state.rank, 2)
        self.assertEqual(state.new, False)

    @freeze_time("2020-07-25")
    def put_card_rank_7(self):
        self.state.rank = 7
        self.state.save()

    @freeze_time("2021-07-25")
    def test_deck_post_rank_7(self):
        self.client.login(username='testuser', password='12345')
        self.put_card_rank_7()
        self.client.post(reverse('memory', args={self.deck.id}), {'form_text': "bbbb"})
        state = CardsState.objects.get(pk=self.state.id)
        self.assertEqual(state.rank, 7)

    def test_deck_post_failure(self):
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('memory', args={self.deck.id}), {'form_text': "cccc"})
        state = CardsState.objects.get(pk=self.state.id)
        self.assertNotEqual(state.side, self.state.side)
        self.assertEqual(state.rank, 1)

    @freeze_time("2020-07-25")
    def put_card_rank_2(self):
        self.state.rank = 2
        self.state.save()

    @freeze_time("2020-07-27")
    def test_deck_post_failure(self):
        self.put_card_rank_2()
        rank = self.state.rank

        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('memory', args={self.deck.id}), {'form_text': "cccc"})

        state = CardsState.objects.get(pk=self.state.id)
        self.assertNotEqual(state.side, self.state.side)
        self.assertEqual(state.rank, rank - 1)


class QuickMemoryTestCase(TestCase):
    def setUp(self):
        user = create_testing_user()
        category = Category.objects.create(name="test", slug="test")

        self.deck = QuickDeck.objects.create(name="test", user=user, category=category)
        card = Cards.objects.create(recto="aaaa", verso="bbbb")
        self.deck.cards.add(card)
        self.state = CardsState.objects.create(deck=self.deck, cards=card, side=True)

    def test_deck_update_page_return_302(self):
        response = self.client.get(reverse('quickmode', args={self.deck.id}))
        self.assertEqual(response.status_code, 302)

    def test_deck_post(self):
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('quickmode', args={self.deck.id}), {'form_text': "bbbb"})
        state = CardsState.objects.get(pk=self.state.id)
        self.assertNotEqual(state.side, self.state.side)
        self.assertEqual(state.rank, 3)

    def test_deck_post_rank_4_and_other_side(self):
        self.state.rank = 4
        self.state.side = not self.state.side
        self.state.save()
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('quickmode', args={self.deck.id}), {'form_text': "aaaa"})
        state = CardsState.objects.get(pk=self.state.id)
        self.assertNotEqual(state.side, self.state.side)
        self.assertEqual(state.rank, 5)

    def test_deck_post_rank_6(self):
        self.state.rank = 6
        self.state.save()
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('quickmode', args={self.deck.id}), {'form_text': "bbbb"})
        state = CardsState.objects.get(pk=self.state.id)
        self.assertEqual(state.rank, 7)

    def test_deck_post_failure(self):
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('quickmode', args={self.deck.id}), {'form_text': "cccc"})
        state = CardsState.objects.get(pk=self.state.id)
        self.assertNotEqual(state.side, self.state.side)
        self.assertEqual(state.rank, 2)

    def test_deck_post_incomplete(self):
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('quickmode', args={self.deck.id}), {'form_text': "bb"})
        state = CardsState.objects.get(pk=self.state.id)
        self.assertNotEqual(state.side, self.state.side)
        self.assertEqual(state.rank, 2)

    def test_deck_post_failure_rank_6(self):
        self.state.rank = 6
        self.state.save()
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('quickmode', args={self.deck.id}), {'form_text': "cccc"})
        state = CardsState.objects.get(pk=self.state.id)
        self.assertEqual(state.rank, 1)
