from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth import authenticate
from django.forms import *

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
            return HttpResponseRedirect('/app/')
    else:
        form = UserForm()

    return render(request, 'adduser.html', {'form': form})

def fda_authenticate(request):

	if request.method == "GET":

		usr = request.GET['username']
		pwd = request.GET['password']

		user = authenticate(username=usr, password=pwd)

		#default_report = Report.objects.create(reportName="Default Report", companyUser=user)

		if user is not None:
			return HttpResponse("You have logged in successfully!")
		else:
			return HttpResponse("Invalid Login Credentials.")

def get_reports(request):

	if request.method == "GET":

		usr = request.GET['username']
		pwd = request.GET['password']

		user = authenticate(username=usr, password=pwd)

		if user is not None:

			user_reports = Report.objects.filter(companyUser=user)
			report_list = ""

			for x in user_reports:
				report_list += '\t'
				report_list += str(x)
				report_list += '\n'
				#x.delete()

			return HttpResponse(report_list)
		else:
			return HttpResponse("Invalid User.")

class reports(generic.ListView):
    model = Report
    paginate_by = 10
    context_object_name = 'user_reports'
    queryset = Report.objects.all()
    template_name = 'report_list.html'

class groups(generic.ListView):
    model = Report
    paginate_by = 10
    context_object_name = 'groups'
    queryset = UserMadeGroup.objects.all()
    template_name = 'group_list.html'


def add_report(request):
    if request.method == "POST":
        modelForm = ReportForm(request.POST)
        if modelForm.is_valid():
            obj = modelForm.save(commit=False)
            obj.companyUser = request.user
            obj.save()
            modelForm = ReportForm()
    else:
        modelForm = ReportForm()

    return render(request, 'add_report.html', {'modelForm': modelForm})


class reportDetail(generic.DetailView):
    model = Report
    template_name = 'report_detail.html'
