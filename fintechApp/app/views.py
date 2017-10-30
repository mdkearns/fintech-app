from django.shortcuts import render

# Create your views here.
from .models import CustomUser

def index(request):
    """
    View Function for home page of site
    """

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'registration/login.html'
    )

def logout(request):
    return render(
        request,
        'registration/logged_out.html'
    )
