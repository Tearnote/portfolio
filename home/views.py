import random

from django.shortcuts import render
from django.views.decorators.http import require_safe

from projects import models


@require_safe
def index(request):
    """Render the frontpage"""

    # Retrieve random testimonials
    testimonials = models.Testimonial.objects.order_by('?')[:3]

    context = {
        'testimonials': testimonials,
    }
    return render(request, "home/index.html", context)
