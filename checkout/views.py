import stripe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
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
        receipt_email=project.user.email,
        automatic_payment_methods={
            'enabled': True,
        },
        metadata={
            'project_id': project.id,
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


@login_required
@require_safe
def checkout_complete(request):
    """Render the checkout complete page
    """

    context = {
        'stripe_publishable_key': portfolio.settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'checkout/complete.html', context)


@csrf_exempt
@require_POST
def webhook(request):
    """Handle Stripe webhook
    """

    # Retrieve webhook components
    payload = request.body
    signature = request.headers['STRIPE_SIGNATURE']
    endpoint_secret = portfolio.settings.STRIPE_WEBHOOK_SECRET

    # Construct the webhook event
    try:
        event = stripe.Webhook.construct_event(
            payload, signature, endpoint_secret
        )
    except ValueError as e:
        return HttpResponseBadRequest(f'Invalid payload: {str(e)}')
    except stripe.error.SignatureVerificationError as e:
        return HttpResponseBadRequest(f'Signature verification error: {str(e)}')

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        # Retrieve related project
        payment_intent = event['data']['object']
        project_id = payment_intent['metadata']['project_id']
        project = get_object_or_404(models.Project, pk=project_id)

        # Update project status
        if project.status == models.Project.PAYABLE:
            project.status = models.Project.IN_PROGRESS
            project.save()

        # Send email notification to project and website owner
        email_context = {
            'creator': project.user,
            'project': project,
        }

        user_email = (
            render_to_string(
                'checkout/email/project_paid_user_subject.txt',
                email_context, request
            ).strip(),
            render_to_string(
                'checkout/email/project_paid_user_message.txt',
                email_context, request
            ),
            None,
            [project.user.email],
        )
        owner_email = (
            render_to_string(
                'checkout/email/project_paid_owner_subject.txt',
                email_context, request
            ).strip(),
            render_to_string(
                'checkout/email/project_paid_owner_message.txt',
                email_context, request
            ),
            None,
            [owner.email for owner in User.objects.filter(is_staff=True)],
        )

        send_mass_mail((user_email, owner_email))

    # Return success
    return HttpResponse('Webhook processed')
