from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import models, forms


@login_required
def dashboard(request):
    """Render the user/owner dashboard
    """

    # Check if user is the website owner
    is_owner = request.user.is_staff

    # Retrieve all projects for website owner,
    # or only owned projects for regular user
    if is_owner:
        projects = models.Project.objects.all()
    else:
        projects = models.Project.objects.filter(user=request.user)

    context = {
        'projects': projects,
        'is_owner': is_owner,
    }
    return render(request, 'projects/dashboard.html', context)


@login_required
def new_project(request):
    """Render the new project page
    """

    # Create form for new project
    form = forms.ProjectForm()

    context = {
        'form': form,
    }
    return render(request, 'projects/new_project.html', context)
