from django.db import models
from django.conf import settings

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
    private = models.BooleanField(verbose_name="private", default=False)
    favorite = models.BooleanField(verbose_name="favorite", default=False)

    def __str__(self):
        return self.name

    def get_image_name(self):
        return os.path.basename(self.image.image.name)


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
