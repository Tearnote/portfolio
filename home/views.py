import random

from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe, require_http_methods
from django.contrib import messages

from home import forms
from projects import models


@require_safe
def index(request):
    """Render the frontpage
    """

    # Retrieve random testimonials
    testimonials = models.Testimonial.objects.order_by('?')[:3]

    context = {
        'testimonials': testimonials,
    }
    return render(request, 'home/index.html', context)


def submit_contact(request):
    """Apply changes to user profile
    """

    # Create form from POST data and send email to owner
    form = forms.ContactForm(request.POST)
    if form.save():
        messages.info(request,
                      'Message sent successfully, thank you for getting in'
                      ' touch!')
        return redirect('home')
    else:
        messages.error(request,
                       'Message send failed. Please make sure your fields are'
                       ' valid, and try again later.')
        return redirect('contact')


def render_contact(request):
    """Render the contact form page
    """

    # Create form from user's current profile
    form = forms.ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'home/contact.html', context)


@require_http_methods(['GET', 'HEAD', 'POST'])
def contact(request):
    """Dispatch user profile requests
    """

    if request.method == 'POST':
        return submit_contact(request)
    else:
        return render_contact(request)


@require_safe
def privacy_policy(request):
    """Render the privacy policy page
    """

    return render(request, 'home/privacy_policy.html')


@require_safe
def terms_of_service(request):
    """Render the terms of service page
    """

    return render(request, 'home/terms_of_service.html')
