from django.shortcuts import render
from .forms import *
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

# create default reports for testing the FDA
def make_reports(request):

	if request.method == "GET":

		usr = request.GET['username']
		pwd = request.GET['password']

		user = authenticate(username=usr, password=pwd)

		if user is not None:
			num = 1
			Report.objects.create(reportName="Report " + str(num), companyUser=user)
			num += 1
			Report.objects.create(reportName="Report " + str(num), companyUser=user)

			return HttpResponse("Successfully created default reports.")
		else:
			return HttpResponse("Unsuccessfully created default reports.")

def get_reports(request):

	if request.method == "GET":

		usr = request.GET['username']
		pwd = request.GET['password']

		user = authenticate(username=usr, password=pwd)

		if user is not None:

			user_reports = Report.objects.filter(companyUser=user)
			report_list = ""

			for x in user_reports:
				if str(x)[-7:] == "Private":
					report_list += str(x)[:-7]
					report_list += ','
				else:
					report_list += str(x)
					report_list += ','
				#x.delete()

			report_list = report_list[:-1]

			return HttpResponse(report_list)
		else:
			return HttpResponse("Invalid User.")

def display_report(request):

	if request.method == "GET":

		usr = request.GET['username']
		pwd = request.GET['password']
		report_name = request.GET['report']

		user = authenticate(username=usr, password=pwd)

		if user is not None:

			user_report = Report.objects.filter(reportName=report_name, companyUser=user)
			report_text = ""

			for x in user_report:
				user_report = x.display_for_fda()

			report_text += "\tReport: " + report_name + "\n"
			report_text += "\tCreated by: " + str(usr) + "\n"

			return HttpResponse(user_report)
		else:
			return HttpResponse("Invalid User.")


class reports(generic.ListView):
    model = Report
    paginate_by = 10
    context_object_name = 'user_reports'
    queryset = Report.objects.all()
    template_name = 'report_list.html'

class groups(generic.ListView):
    model = UserMadeGroup
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

def suspend_user(request):
    if request.method == "POST":
        form = SuspendUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            sus = form.cleaned_data['action']
            if sus in {'S', 'Suspend'}:
                user.profile.suspended = True
                user.save()
                return render(request, 'suspend_user_success.html', {'form': form})
            if sus == 'U':
                user.profile.suspended = False
                user.save()
                return render(request, 'unsuspend_user_success.html', {'form': form})
    else:
        form = SuspendUserForm()
    return render(request, 'suspend_user.html', {'form': form})

class group_detail(generic.DetailView):
    model = UserMadeGroup
    context_object_name = 'group'
    template_name = 'group_detail.html'

def add_group(request):
    if request.method == "POST":
        form = UserMadeGroupForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data.get('group_name')
            members = form.cleaned_data.get('members')

            new_group = UserMadeGroup.objects.create(group_name=group_name)
            for member in members:
                new_group.members.add(member)
            current_user = request.user
            new_group.members.add(current_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect(reverse('groups'))
    else:
        form = UserMadeGroupForm()

    return render(request, 'add_group.html', {'form': form})
