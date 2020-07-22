from django import forms
from memory_app.models import Category


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(required=False)
    quick_mode = forms.BooleanField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    private = forms.BooleanField(required=False)


class CopyDeck(forms.Form):
    title = forms.CharField(max_length=50)
    quick_mode = forms.BooleanField(required=False)
    private = forms.BooleanField(required=False)


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
