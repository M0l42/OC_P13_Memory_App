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


class Cards(models.Model):
    recto = models.CharField(verbose_name='recto', max_length=200)
    verso = models.CharField(verbose_name='verso', max_length=200)


class Desk(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    name = models.CharField(verbose_name='name', max_length=200)
    cards = models.ManyToManyField(Cards)


class CardsState(models.Model):
    cards = models.ForeignKey(Cards, on_delete=models.CASCADE, default=None)
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, default=None)
    date = models.DateField(auto_now=False, auto_now_add=False)
    rank = models.IntegerField(
        verbose_name="rank",
        default=0,
        choices=RANK,
    )
    side = models.BooleanField(verbose_name="side")
