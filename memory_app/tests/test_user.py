from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from . import create_testing_user


class SignUpTestCase(TestCase):
    def setUp(self):
        self.form = {'username': "test",
                     "first_name": "nathan",
                     "last_name": "boukobza",
                     "email": "email@email.com",
                     "password": "123456"}

    def test_sign_up_valid(self):
        old_accounts = User.objects.count()
        self.form["confirm_password"] = "123456"
        self.client.post(reverse('sign-up'), self.form)
        new_accounts = User.objects.count()
        self.assertEqual(new_accounts, old_accounts + 1)

    def test_sign_up_non_valid(self):
        old_accounts = User.objects.count()
        self.form["confirm_password"] = "abcde"
        self.client.post(reverse('sign-up'), self.form)
        new_accounts = User.objects.count()
        self.assertEqual(new_accounts, old_accounts)


class LogInTestCase(TestCase):
    def setUp(self):
        create_testing_user()

    def test_log_in_success(self):
        self.client.post(reverse('login'), {"username": "testuser", "password": "12345"})
        user = auth.get_user(self.client)
        assert user.is_authenticated

    def test_log_in_failure(self):
        self.client.post(reverse('login'), {"username": "testuser", "password": "123456"})
        user = auth.get_user(self.client)
        assert not user.is_authenticated


class LogOffTestCase(TestCase):
    def setUp(self):
        create_testing_user()

    def test_log_off(self):
        self.client.login(username='testuser', password='12345')
        self.client.get(reverse('log-off'))
        user = auth.get_user(self.client)
        assert not user.is_authenticated

    def test_log_off_302(self):
        response = self.client.get(reverse('log-off'))
        self.assertEqual(response.status_code, 302)


class EditAccountPageTestCase(TestCase):
    def setUp(self):
        create_testing_user()

    def test_edit_page_returns_302(self):
        response = self.client.get(reverse('edit-account'))
        self.assertEqual(response.status_code, 302)

    def test_edit_mail(self):
        self.client.login(username='testuser', password='12345', email="test@test.com")
        self.client.post(reverse('edit-account'), {"email": "email@email.com"})
        user = auth.get_user(self.client)
        self.assertEqual(user.email, "email@email.com")
