from memory_app.models import Cards, Deck, CardsState, QuickModeDeck
from memory_app.forms.load import UploadFileForm, ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
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
        for i in range(len(recto)):
            card = Cards.objects.create(recto=recto[i], verso=verso[i])
            deck.cards.add(card)
            CardsState.objects.create(deck=deck, cards=card, rank=1, side=True)

        return super().form_valid(form)


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['boukobza.nathan@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "memory_app/contact_form.html", {'form': form})


def success_view(request):
    return HttpResponse('Success! Thank you for your message.')
