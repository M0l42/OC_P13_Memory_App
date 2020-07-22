from django.db import models
from django.conf import settings


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


class Deck(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    name = models.CharField(verbose_name='name', max_length=200)
    cards = models.ManyToManyField(Cards)
    created_at = models.DateField(auto_now_add=True)
    favorite = models.BooleanField(verbose_name="favorite", default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    private = models.BooleanField(verbose_name="private", default=False)

    def __str__(self):
        return self.name


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


class QuickModeDeck(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, default=None)
    rank = models.IntegerField(
        verbose_name="rank",
        default=1,
        choices=RANK,
    )
