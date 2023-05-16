from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect

from . import models, forms


def edit_profile(request):
    """Apply changes to user profile
    """

    # Create form from POST data and save changes
    userprofile = request.user.profile
    form = forms.ProfileForm(request.POST, instance=userprofile)
    userprofile = form.save()
    messages.info(request, 'Profile edited successfully!')

    return redirect('dashboard')


def render_profile(request):
    """Render the profile edit page
    """

    # Create form from user's current profile
    userprofile = request.user.profile
    form = forms.ProfileForm(instance=userprofile)

    context = {
        'form': form,
    }
    return render(request, 'userprofile/profile.html', context)


@login_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def profile(request):
    """Dispatch user profile requests
    """

    if request.method == 'POST':
        return edit_profile(request)
    else:
        return render_profile(request)
