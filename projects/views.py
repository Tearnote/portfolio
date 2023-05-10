from django.shortcuts import render
from . import models


def dashboard(request):
    """Render the user/owner dashboard"""

    # Retrieve all projects
    projects = models.Project.objects.all()

    context = {
        'projects': projects,
    }
    return render(request, "projects/dashboard.html", context)
