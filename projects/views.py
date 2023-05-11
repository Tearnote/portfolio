from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
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


@login_required
def cancel_project(request):
    """Set project state to cancelled
    """

    # Confirm request is valid
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    # Confirm user is the website owner or owns the project being cancelled
    project = get_object_or_404(models.Project, pk=request.POST['projectId'])
    if not request.user.is_staff and project.user != request.user:
        return HttpResponseForbidden()

    project.status = models.Project.CANCELLED
    project.save()

    return redirect('dashboard')


@login_required
def reject_project(request):
    """Set project state to rejected
    """

    # Confirm request is valid
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_staff:
        return HttpResponseForbidden()

    project = get_object_or_404(models.Project, pk=request.POST['projectId'])
    project.status = models.Project.REJECTED
    project.save()

    return redirect('dashboard')
