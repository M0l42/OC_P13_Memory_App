from django.contrib.auth.models import User
from purebeurre.models import UserInfos
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from purebeurre.forms.login import SignUpForm, LogInForm
from purebeurre.forms.edit import EditAccountForm
from django.views import View
from django.views.generic.edit import FormView

import os


class SignUpFormView(FormView):
    """
    A class of FormView to register a new user

    ...

    Attributes
    ----------
    template_name : str
        the name of the template
    form_class : SignUpForm
        Form of the view
    success_url : str
        url of the success page

    Methods
    -------
    get_context_data(**kwargs):
        Get the context of the view
    form_valid(form):
        Register the new user

    """
    form_class = SignUpForm
    template_name = 'pure_beurre/form.html'
    success_url = '/login/'

    def get_context_data(self, **kwargs):
        """
        Call the original method of the view and add the title on the context

        Parameters
        ----------
        kwargs : str
            Some argument that Django are passing, need when call the original method of the view

        Returns
        -------
        dict
            a dict of the context of the page
        """
        context = super(SignUpFormView, self).get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context

    def form_valid(self, form):
        """
        Get all the data the user filled up
        Only register if the two password are the same
        Ask to filled it up again if it's not

        Parameters
        ----------
        form : Form
            A form with the data filled by the user

        Returns
        -------
        form_valid()
            a function who render a page to the success url

        """
        user_name = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']
        context = self.get_context_data()
        context['error'] = ''

        try:
            User.objects.get(username=user_name)
            context['error'] = "Le nom d'utilisateur est déjà pris"
            return render(self.request, self.template_name, context=context)
        except ObjectDoesNotExist:
            if password == confirm_password:
                user = User.objects.create_user(username=user_name, email=email, password=password)
                UserInfos.objects.create(user=user)
            else:
                context['error'] = 'Les deux mots de passe ne sont pas les mêmes'
                return render(self.request, self.template_name, context=context)

        return super().form_valid(form)


class LogInFormView(FormView):
    """
    A class of FormView to logged in the user

    ...

    Attributes
    ----------
    template_name : str
        the name of the template
    form_class : SignUpForm
        Form of the view
    success_url : str
        url of the success page

    Methods
    -------
    get_context_data(**kwargs):
        Get the context of the view
    form_valid(form):
        Logged in the user

    """
    form_class = LogInForm
    template_name = 'pure_beurre/form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        """
        Call the original method of the view and add the title on the context

        Parameters
        ----------
        kwargs : str
            Some argument that Django are passing, need when call the original method of the view

        Returns
        -------
        dict
            a dict of the context of the page
        """
        context = super(LogInFormView, self).get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def form_valid(self, form):
        """
        Get all the data the user filled up
        Log the user in if the user and the password are correct
        Ask again if not

        Parameters
        ----------
        form : Form
            A form with the data filled by the user

        Returns
        -------
        form_valid()
            a function who render a page to the success url

        """
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        context = self.get_context_data()

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            context['error'] = "Votre nom d'utilisteur ou votre Mot de passe est incorrect"
            return render(self.request, self.template_name, context=context)

        return super().form_valid(form)


class LogOutView(LoginRequiredMixin, RedirectView):
    """
    A class of LoginRequiredMixin and RedirectView to log off the user

    ...

    Attributes
    ----------
    login_url : str
        The url of the login page
    pattern_name : str
        name of the path we want to redirect to

    Methods
    -------
    get_redirect_url(*args, **kwargs):
        Log the user out
    """

    login_url = '/login/'
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        """
        Log the user out

        Parameters
        ----------
        args : str
            Some argument that Django are passing
        kwargs : str
            Other argument that Django are passing

        Returns
        -------
        get_redirect_url
            a function that redirect to a specific page
        """
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class AccountView(LoginRequiredMixin, View):
    """
    A class of LoginRequiredMixin and View to show the account Info

    ...

    Attributes
    ----------
    login_url : str
        The url of the login page
    template_name : str
        the name of the template

    Methods
    -------
    get(*args, **kwargs):
        get the current user and his info
    """

    login_url = '/login/'
    template_name = 'pure_beurre/account.html'

    def get(self, *args, **kwargs):
        """
        Log the user out

        Parameters
        ----------
        args : str
            Some argument that Django are passing
        kwargs : str
            Other argument that Django are passing

        Returns
        -------
        render
            a function that render the page with everything it need as the template name and it context
        """
        context = dict()
        context['title'] = 'Account'
        context['user'] = self.request.user
        try:
            context['user_info'] = UserInfos.objects.get(user=self.request.user)
            _, file_extension = os.path.splitext(context['user_info'].image.name)
            context['extension'] = file_extension
        except ObjectDoesNotExist:
            context['user_info'] = UserInfos.objects.create(user=self.request.user)

        return render(self.request, self.template_name, context=context)


class EditAccountFormView(LoginRequiredMixin, FormView):
    """
    A class of LoginRequiredMixin and FormView to allow users to change some of theirs infos

    ...

    Attributes
    ----------
    login_url : str
        The url of the login page
    template_name : str
        the name of the template
    form_class : EditAccountForm
        Form of the view
    success_url : str
        url of the success page

    Methods
    -------
    get_context_data(**kwargs):
        Get the context of the view
    form_valid(form):
        Change all the info the users filled

    """
    login_url = '/login/'
    form_class = EditAccountForm
    template_name = 'pure_beurre/form.html'
    success_url = '/account/'

    def get_context_data(self, **kwargs):
        """
        Call the original method of the view and add the title on the context

        Parameters
        ----------
        kwargs : str
            Some argument that Django are passing, need when call the original method of the view

        Returns
        -------
        dict
            a dict of the context of the page
        """

        context = super(EditAccountFormView, self).get_context_data(**kwargs)
        context['title'] = 'Edit Account'
        return context

    def form_valid(self, form):
        """
        Get all the data the user filled up
        Change email if there's a new one
        Change email if there's a new one, delete the old one

        Parameters
        ----------
        form : Form
            A form with the data filled by the user

        Returns
        -------
        form_valid()
            a function who render a page to the success url

        """
        image = form.cleaned_data['image']
        email = form.cleaned_data['email']

        user = self.request.user
        if image:
            info = UserInfos.objects.get(user=user)
            os.remove(info.image.path)
            info.image = image
            info.save()
        if email:
            user.email = email
            user.save()

        return super().form_valid(form)
