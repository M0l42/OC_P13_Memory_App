from django import forms


class SignUpForm(forms.Form):
    """
    Form to collect all the infos we need to register a new user
    """
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class LogInForm(forms.Form):
    """
    Form to log in a user
    """
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class EditAccountForm(forms.Form):
    """
    Form to collect all the infos we need to register a new user
    """
    email = forms.EmailField(required=False)
