from django.test import TestCase
from django.urls import reverse


class HomePageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class LegalMentionsPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('legal-mention'))
        self.assertEqual(response.status_code, 200)
