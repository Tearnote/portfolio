from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
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


def render_new_project(request):
    """Render the new project page
    """

    # Create form for new project
    form = forms.ProjectForm()

    context = {
        'form': form,
    }
    return render(request, 'projects/new_project.html', context)


def create_new_project(request):
    """Create a new Project from POST data
    """

    # Construct form from POST data
    form = forms.ProjectForm(request.POST)
    project = form.save(commit=False)
    project.user = request.user
    project.save()

    return redirect('dashboard')


@login_required
def new_project(request):
    """Dispatch new project requests
    """

    if request.method == 'GET':
        return render_new_project(request)
    elif request.method == 'POST':
        return create_new_project(request)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
