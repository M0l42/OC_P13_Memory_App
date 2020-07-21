from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests


def home_view(requests):
    """ render the home page """
    return render(requests, 'memory_app/home_page.html', context={'title': 'Home'})


def legal_mentions(requests):
    """ render the legal mentions page """
    return render(requests, 'memory_app/mention-legal.html', context={'title': 'Mentions légale'})

