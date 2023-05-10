from django.shortcuts import render


def dashboard(request):
    """Render the user/owner dashboard"""

    return render(request, "projects/dashboard.html")
