import random

from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe, require_http_methods

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
    return render(request, "home/index.html", context)


def submit_contact(request):
    """Apply changes to user profile
    """

    # Create form from POST data and send email to owner
    form = forms.ContactForm(request.POST)
    form.save()

    return redirect('home')


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
