from memory_app.models import Cards, Deck, CardsState, QuickModeDeck
from memory_app.forms.load import UploadFileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
import csv
from io import TextIOWrapper


class UploadCSVFormView(LoginRequiredMixin, FormView):
    form_class = UploadFileForm
    template_name = 'memory_app/form.html'
    success_url = '/deck/'

    def form_valid(self, form):
        name = form.cleaned_data['title']
        file = form.cleaned_data['file']
        quick_mode = form.cleaned_data['quick_mode']
        category = form.cleaned_data['category']
        user = self.request.user

        deck = Deck.objects.create(name=name, user=user, category=category)
        if quick_mode:
            QuickModeDeck.objects.create(deck=deck)

        if file:
            f = TextIOWrapper(file, encoding=self.request.encoding)
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                card = Cards.objects.create(recto=row[0], verso=row[1])
                deck.cards.add(card)
                CardsState.objects.create(deck=deck, cards=card, rank=1, side=True)

        recto = self.request.POST.getlist('recto')
        verso = self.request.POST.getlist('verso')
        for i in range(len(name)):
            card = Cards.objects.create(recto=recto[i], verso=verso[i])
            deck.cards.add(card)
            CardsState.objects.create(deck=deck, cards=card, rank=1, side=True)

        return super().form_valid(form)
