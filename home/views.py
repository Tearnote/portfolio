from django.shortcuts import render


def index(request):
    """Render the frontpage"""

    return render(request, "home/index.html")
