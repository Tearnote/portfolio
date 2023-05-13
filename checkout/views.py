import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST, require_safe

import portfolio.settings
from projects import models


@login_required
@require_POST
def create_payment_intent(request):
    """Create a Stripe Payment Intent for a project
    in a payable state
    """

    # Retrieve the payable project
    project = get_object_or_404(models.Project, pk=request.POST['project_id'])
    if project.status != models.Project.PAYABLE or project.user != request.user:
        return HttpResponseBadRequest()

    # Create the Payment Intent
    intent = stripe.PaymentIntent.create(
        amount=project.quote_amount * 100,
        currency='eur',
        automatic_payment_methods={
            'enabled': True,
        },
    )

    return JsonResponse({
        'clientSecret': intent['client_secret'],
    })


@login_required
@require_safe
def checkout(request, project_id):
    """Render the checkout page
    """

    # Retrieve the payable project
    project = get_object_or_404(models.Project, pk=project_id)
    if project.status != models.Project.PAYABLE or project.user != request.user:
        return HttpResponseBadRequest()

    context = {
        'project': project,
        'stripe_publishable_key': portfolio.settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'checkout/checkout.html', context)
