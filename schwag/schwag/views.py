from django.contrib import messages
from django.contrib.auth import get_user_model, logout as logout_user, login as login_user, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from .forms import ContactForm, LoginForm, RegistrationForm


import logging
logger = logging.getLogger("default")


def home(request, template_name='home.html'):
    context = {}
    return render_to_response(template_name, context, RequestContext(request))


def login(request, template_name='login.html'):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.login(request):
            messages.success(request, "You have successfully logged in.")
            return redirect(request.POST.get('next', '/'))
        else:
            messages.error(request, "Your username and password do not match.")
    else:
        form = LoginForm()
    return render_to_response(template_name, {'form': form, }, RequestContext(request))


def logout(request):
    logout_user(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


def register(request, template_name='register.html'):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #process the form
            email = request.POST.get('email', None)
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            password = request.POST.get('password', None)
            user = get_user_model().objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            user.save()
            user = authenticate(username=email, password=password)
            login_user(request, user)
            messages.success(request, "You have successfully registered and are now logged in.")
            return redirect(request.POST.get('next', '/'))
    else:
        initial = {'email': request.GET.get('email', None)}
        form = RegistrationForm(initial=initial)
    context = {'form': form, 'next': request.GET.get('next', None), }
    return render_to_response(template_name, context, RequestContext(request))
