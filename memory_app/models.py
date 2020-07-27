from django.db import models
from django.conf import settings

from datetime import date, timedelta
import os


RANK = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
]


class Category(models.Model):
    name = models.CharField(verbose_name='name', max_length=200)
    slug = models.SlugField(verbose_name='slug', max_length=200)

    def __str__(self):
        return self.name


class Cards(models.Model):
    recto = models.CharField(verbose_name='recto', max_length=200)
    verso = models.CharField(verbose_name='verso', max_length=200)

    def __str__(self):
        return self.recto + " - " + self.verso


def photo_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return 'memory_app/static/img/deck/{basename}{file_extension}'.format(
        basename=base_filename, file_extension=file_extension)


class DeckImage(models.Model):
    name = models.CharField(verbose_name='name', max_length=200)
    image = models.ImageField(upload_to=photo_path)

    def __str__(self):
        return self.name


class Deck(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    name = models.CharField(verbose_name='name', max_length=200)
    cards = models.ManyToManyField(Cards)
    created_at = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    image = models.ForeignKey(DeckImage, on_delete=models.CASCADE, default=None, blank=True, null=True)
    color = models.CharField(verbose_name='color', max_length=7, blank=True, null=True, default='#ffc728')
    color_text = models.CharField(verbose_name='color_text', max_length=7, blank=True, null=True, default='#000000')
    private = models.BooleanField(verbose_name="private", default=False)
    favorite = models.BooleanField(verbose_name="favorite", default=False)

    def __str__(self):
        return self.name

    def get_image_name(self):
        return os.path.basename(self.image.image.name)

    def get_card(self):
        today = date.today()
        new_card = None
        for card in CardsState.objects.filter(deck=self):
            if card.rank == 1:
                if card.date != today or card.new is True:
                    new_card = card
                    break
            if card.rank == 2:
                if card.date == today - timedelta(days=2):
                    new_card = card
                    break
            if card.rank == 3:
                if today.weekday() == 0:
                    new_card = card
                    break
            if card.rank == 4:
                if today.day == 1:
                    new_card = card
                    break
            if card.rank == 5:
                if today >= self.created_at.replace(month=self.created_at.month + 3):
                    new_card = card
                    break
            if card.rank == 6:
                try:
                    if today >= self.created_at.replace(month=self.created_at.month + 6):
                        new_card = card
                        break
                except ValueError:
                    if today >= self.created_at.replace(month=self.created_at.month - 6, year=self.created_at.year + 1):
                        new_card = card
                        break
            if card.rank == 7:
                if today >= self.created_at.replace(year=self.created_at.year + 1):
                    new_card = card
                    break
        return new_card

    def update(self):
        state = self.get_card()
        context = dict()
        try:
            card = state.cards
            context['deck'] = self
            if state.side:
                context['recto'] = card.recto
                context['verso'] = card.verso
            else:
                context['recto'] = card.verso
                context['verso'] = card.recto
        except AttributeError:
            context['error'] = "No more cards"
        return context


class CardsState(models.Model):
    cards = models.ForeignKey(Cards, on_delete=models.CASCADE, default=None)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, default=None)
    date = models.DateField(auto_now=True)
    rank = models.IntegerField(
        verbose_name="rank",
        default=1,
        choices=RANK,
    )
    side = models.BooleanField(verbose_name="side")
    new = models.BooleanField(verbose_name="new", default=True)


class QuickDeck(Deck):
    rank = models.IntegerField(
        verbose_name="rank",
        default=1,
        choices=RANK,
    )

    def get_card(self):
        try:
            new_card = CardsState.objects.filter(deck=self, rank=self.rank)[0]
        except IndexError:
            if self.rank < 6:
                self.rank += 1
            else:
                self.rank = 1
                for state in CardsState.objects.filter(deck=self, rank=7):
                    state.rank = 5
                    state.save()
            self.save()
            new_card = self.get_card()
        return new_card
