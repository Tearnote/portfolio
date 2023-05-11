from django.shortcuts import render
from django.views.decorators.http import require_safe


@require_safe
def index(request):
    """Render the frontpage"""

    return render(request, "home/index.html")
