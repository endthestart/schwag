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


def about(request, template_name='about.html'):
    context = {}
    return render_to_response(template_name, context, RequestContext(request))


def location(request, template_name='location.html'):
    context = {}
    return render_to_response(template_name, context, RequestContext(request))


def contact(request, template_name='contact.html'):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender_email = form.cleaned_data['sender_email']
            sender_name = form.cleaned_data['sender_name']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@senexcycling.com']
            if cc_myself:
                recipients.append(sender_email)

            from django.core.mail import send_mail

            email_message = "A new message from: {0}<br /><br />{1}".format(sender_name, message)

            send_mail(subject, email_message, sender_email, recipients)
            return HttpResponseRedirect('/contact/thanks/')

    context = {
        'form': form,
    }

    return render_to_response(template_name, context, RequestContext(request))


def contact_thanks(request, template_name="contact_thanks.html"):
    return render_to_response(template_name, {}, RequestContext(request))


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
