from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.views import generic

# Create your views here.
from .models import *

def index(request):
    """
    View Function for home page of site
    """

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html'
    )

def adduser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            pw = form.cleaned_data.get('password1')
            group = form.cleaned_data.get('user_type')
            g = Group.objects.get(name=group)

            new_user = User.objects.create_user(username,email,pw)
            g.user_set.add(new_user)
            login(request, new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('index')
    else:
        form = UserForm()

    return render(request, 'adduser.html', {'form': form})
	
def fda_authenticate(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			return HttpResponse("You have logged in successfully!")
	
	return HttpResponse("Invalid Login Credentials.")


class reports(generic.ListView):
    model = Report
    paginate_by = 2
    context_object_name = 'user_reports'
    queryset = Report.objects.all()
    template_name = 'report_list.html'