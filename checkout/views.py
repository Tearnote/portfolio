from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

from projects import models


def checkout(request, project_id):
    """Render the checkout page
    """

    # Retrieve the payable project
    project = get_object_or_404(models.Project, pk=project_id)
    if project.status != models.Project.PAYABLE:
        return HttpResponseBadRequest()

    context = {
        'project': project,
    }
    return render(request, 'checkout/checkout.html', context)
