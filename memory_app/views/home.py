from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests


def home_view(requests):
    """ render the home page """
    return render(requests, 'pure_beurre/home.html', context={'title': 'Home'})