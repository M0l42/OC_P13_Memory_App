from django.test import TestCase
from django.urls import reverse
from memory_app.forms.load import UploadFileForm, ContactForm
from django.core.files.uploadedfile import SimpleUploadedFile
from memory_app.models import Cards, CardsState, Deck, QuickModeDeck, Category, DeckImage
from . import create_testing_user


class DeckMenuTestCase(TestCase):
    def setUp(self):
        create_testing_user()
        category = Category.objects.create(name="test", slug="test")
        data = {
            "title": "test",
            "category": category
        }
        self.form = UploadFileForm(data=data)

    def test_deck_menu_page_return_302(self):
        response = self.client.get(reverse('update'))
        self.assertEqual(response.status_code, 302)

    def test_add_cards(self):
        user = self.client.login(username='testuser', password='12345')
        old_deck = Deck.objects.filter(user=user).count()
        self.client.post(reverse('update'), self.form)
        print(Deck.objects.all())
        new_deck = Deck.objects.all().count()
        self.assertEqual(new_deck, old_deck + 1)

    def test_form(self):
        category = Category.objects.create(name="test", slug="test")
        data = {
            "title": "test",
            "category": category
        }
        form = UploadFileForm(data=data)
        self.assertTrue(form.is_valid())
