from django import forms
from memory_app.models import Category


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(required=False)
    quick_mode = forms.BooleanField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
