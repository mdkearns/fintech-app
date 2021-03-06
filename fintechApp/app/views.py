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
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from time import gmtime, strftime
import json
import operator
from django.db.models import Q
from datetime import datetime
from django.shortcuts import redirect
from django.utils.encoding import smart_bytes, smart_text
from itertools import chain
from django.core.files.base import File
# Create your views here.
from .models import *

if not User.objects.filter(username='administrator').exists():
    user = User.objects.create_user('administrator','email@email.com','pass1010')
    grp = Group.objects.get(name='Site Manager')
    grp.user_set.add(user)

def index(request):
    """
    View Function for home page of site
    """
    starred = []
    if request.user.is_authenticated:
        starred = Report.objects.filter(stars=request.user)

    return render(
        request,
        'index.html',
        {'starred': starred}
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

def get_report_files(request):

	if request.method == "GET":

		usr = request.GET['username']
		pwd = request.GET['password']
		report_name = request.GET['report']

		user = authenticate(username=usr, password=pwd)

		if user is not None:

			f = Report.objects.filter(reportName=report_name, companyUser=user)

			for file in f:
				f = file.get_files()

			files = ReportFile.objects.filter(companyUser=user)
			file_name = "None"

			for file in f:
				file_name = str(file)

			return HttpResponse(file_name)
		else:
			return HttpResponse("Invalid User.")

def download_file(request):

	if request.method == "GET":

		usr = request.GET['username']
		pwd = request.GET['password']
		report_name = request.GET['report']
		file_name = request.GET['file']

		user = authenticate(username=usr, password=pwd)

		if user is not None:

			a = ""

			try:
				with open("files/"+file_name) as f:
					a = f.read()
			except IOError:
				a = "Error."

			return HttpResponse(a)

def upload_file(request):

	if request.method == "GET":

		usr = request.GET['username']
		pwd = request.GET['password']
		report_name = request.GET['report']
		file_contents = request.GET['file']
		file_name = request.GET['dirname']

		user = authenticate(username=usr, password=pwd)

		if user is not None:

			file_to_save = open(file_name, "w")
			file_to_save.write(file_contents)
			file_to_save.close()
			file_to_save = open(file_name, "r")

			report_file = ReportFile(companyUser=user, name=file_name, file=File(file_to_save), encrypted=False)
			report_file.save()

			print(report_file.file)

			report = Report.objects.filter(reportName=report_name, companyUser=user).first()

			report.files.add(report_file)

			return HttpResponse("hello, world")

class reports(generic.ListView):
    model = Report
    paginate_by = 4
    context_object_name = 'user_reports'
    template_name = 'report_list.html'

    def get_queryset(self):
        result = Report.objects.all()

        if(self.request.user.groups.filter(name='Site Manager').exists() == False):
            result = result.filter(Q(accessType = "public") | Q(companyUser = self.request.user)|Q(usermadegroup__members=self.request.user)).distinct()

        return result

class reportSearchListView(generic.ListView):
    model = Report
    paginate_by = 4
    template_name = 'report_list.html'
    context_object_name = 'user_reports'

    def get_queryset(self):
        result = Report.objects.all()

        if(self.request.user.groups.filter(name='Site Manager').exists() == False):
            result = result.filter(Q(accessType = "public") | Q(companyUser = self.request.user) | Q(usermadegroup__members=self.request.user)).distinct()

        reportName = self.request.GET.get('reportName')
        reportNameExact = self.request.GET.get('reportNameExact')
        dateRange = self.request.GET.get('daterange')
        dates = dateRange.split(" - ")
        dateStart = datetime.strptime(dates[0].lower(), '%m/%d/%Y %I:%M %p')
        dateEnd = datetime.strptime(dates[1].lower(), '%m/%d/%Y %I:%M %p')
        companyName = self.request.GET.get('companyName')
        companyNameExact = self.request.GET.get('companyNameExact')
        companyCEO = self.request.GET.get('companyCEO')
        companyCEOExact = self.request.GET.get('companyCEOExact')
        companyLocation = self.request.GET.get('companyLocation')
        companyLocationExact = self.request.GET.get('companyLocationExact')
        companyCountry = self.request.GET.get('companyCountry')
        companyCountryExact = self.request.GET.get('companyCountryExact')
        sector = self.request.GET.get('sector')
        sectorExact = self.request.GET.get('sectorExact')
        industry = self.request.GET.get('industry')
        industryExact = self.request.GET.get('industryExact')
        currentProjects = self.request.GET.get('currentProjects')
        myReports = self.request.GET.get('myReports')
        favorited = self.request.GET.get('favorited')

        if reportNameExact and reportName:
            result = result.filter(reportName = reportName)
        elif reportName:
            result = result.filter(reportName__contains = reportName)
        if dateRange:
            result = result.filter(timeStamp__range= [dateStart, dateEnd])
        if companyNameExact and companyName:
            result = result.filter(companyName = companyName)
        elif companyName:
            result = result.filter(companyName__contains = companyName)
        if companyCEOExact and companyCEO:
            result = result.filter(companyCEO = companyCEO)
        elif companyCEO:
            result = result.filter(companyCEO__contains = companyCEO)
        if companyLocationExact and companyLocation:
            result = result.filter(companyLocation = companyLocation)
        elif companyLocation:
            result = result.filter(companyLocation__contains = companyLocation)
        if companyCountryExact and companyCountry:
            result = result.filter(companyCountry = companyCountry)
        elif companyCountry:
            result = result.filter(companyCountry__contains = companyCountry)
        if sectorExact and sector:
            result = result.filter(sector = sector)
        elif sector:
            result = result.filter(sector__contains = sector)
        if industryExact and industry:
            result = result.filter(industry = industry)
        elif industry:
            result = result.filter(industry__contains = industry)
        if currentProjects:
            result = result.filter(currentProjects__contains = currentProjects)
        if myReports:
            result = result.filter(companyUser = self.request.user)
        if favorited:
            result = result.filter(stars=self.request.user)

        return result

class groups(generic.ListView):
    model = UserMadeGroup
    paginate_by = 4
    context_object_name = 'groups'
    template_name = 'group_list.html'
    def get_queryset(self):
        return UserMadeGroup.objects.filter(members = self.request.user)

class messages(generic.ListView):
    model = Message
    paginate_by = 4
    context_object_name = 'messages'
    template_name = 'view_messages.html'

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

class message_detail(generic.detail.DetailView):
    model = Message
    context_object_name = 'message'
    template_name = 'message_detail.html'


@permission_required('app.add_report')
def add_report(request):
    if request.method == "POST":
        modelForm = ReportForm(request.POST, user=request.user)
        if modelForm.is_valid():
            obj = modelForm.save(commit=False)
            obj.companyUser = request.user
            obj.timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            obj.save()
            modelForm.save_m2m()
            modelForm = ReportForm(user=request.user)
    else:
        modelForm = ReportForm( user=request.user)

    return render(request, 'add_report.html', {'modelForm': modelForm})


def starReport(request, reportId, view):
    url = request.META.get('HTTP_REFERER')

    report = Report.objects.filter(id = reportId).first()
    if request.user in report.stars.all():
        report.stars.remove(request.user)
    else:
        report.stars.add(request.user)

    return HttpResponseRedirect(url)


@permission_required('app.add_report')
def add_reportFile(request):
    if request.method == "POST":
        if("encrypted" in request.POST.keys()):
            if(request.POST['encrypted']):
                request.FILES['file'].open('w+')
                text = request.FILES['file'].read()
                encrypted = request.user.key.encrypt(text)
                request.FILES['file'].seek(0)
                request.FILES['file'].write(encrypted)

        modelForm = ReportFileForm(request.POST, request.FILES)
        if modelForm.is_valid():
            obj = modelForm.save(commit=False)
            obj.companyUser = request.user
            obj.save()
            modelForm = ReportFileForm()
    else:
        modelForm = ReportFileForm()

    return render(request, 'add_ReportFile.html', {'modelForm': modelForm})


def addFileToReport(request,reportId):
    if request.method == "POST":
        form = addFileToReportForm(request.POST, request=request, reportId = reportId)

        if form.is_valid():
            report = Report.objects.filter(id = reportId).first()
            files = form.cleaned_data.get('newFiles')
            print(files)

            for f in files:
                report.files.add(f)

            return HttpResponseRedirect(reverse('reports'))
    else:
        form = addFileToReportForm(request=request, reportId = reportId)
    return render(request, 'add_file_to_report.html', {'form': form, 'reportId': reportId})


def addNewFileToReport(request,reportId):
    if request.method == "POST":
        modelForm = ReportFileForm(request.POST, request.FILES)
        if modelForm.is_valid():
            if("encrypted" in request.POST.keys()):
                if(request.POST['encrypted']):
                    request.FILES['file'].open('w+')
                    text = request.FILES['file'].read()
                    encrypted = request.user.key.encrypt(text)
                    request.FILES['file'].seek(0)
                    request.FILES['file'].write(encrypted)


            obj = modelForm.save(commit=False)
            obj.companyUser = request.user
            obj.save()
            newFile = ReportFile.objects.filter(id = obj.id).first()
            report = Report.objects.filter(id = reportId).first()

            report.files.add(newFile)

            modelForm = ReportFileForm()
    else:
        modelForm = ReportFileForm()

    return render(request, 'add_new_file_to_report.html', {'reportId': reportId, 'modelForm': modelForm})



class reportDetail(generic.DetailView):
    model = Report
    context_object_name = 'report'
    template_name = 'report_detail.html'

    def get_queryset(self):
        queryset = super(reportDetail, self).get_queryset()

        if(self.request.user.groups.filter(name='Site Manager').exists() == False):
            queryset = queryset.filter(Q(accessType = "public") | Q(companyUser = self.request.user) | Q(usermadegroup__members=self.request.user)).distinct()


        return queryset


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

def add_sm(request):
    if request.method == "POST":
        form = AddSMForm(request.POST)
        if form.is_valid():
           user = form.cleaned_data['user']
           group = Group.objects.get(name='Site Manager')
           user.groups.add(group)
           return render(request, 'add_sm_success.html', {'form': form})
    else:
        form = AddSMForm()
    return render(request, 'add_sm.html', {'form': form})

def sm_add_to_group(request):
    if request.method == "POST":
        form = AddToGroupForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            group = form.cleaned_data['group']
            action = form.cleaned_data['action']
            if action == 'A':
                UserMadeGroup.add_user(group, user)
                return render(request, 'sm_add_to_group_success.html', {'form':form})
            if action == 'R':
                UserMadeGroup.remove_user(group, user)
                return render(request, 'sm_remove_from_group_success.html', {'form':form})
            return render(request, 'sm_add_to_group.html', {'form':form})
    else:
        form = AddToGroupForm()
    return render(request, 'sm_add_to_group.html', {'form': form})

class group_detail(generic.detail.DetailView):
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

def remove_from_group(request, groupId):
    current_user = request.user
    UserMadeGroup.objects.filter(id=groupId).first().members.remove(current_user)
    return HttpResponseRedirect(reverse('groups'))

def add_users_to_group(request, groupId):
    groupId = groupId
    if request.method == "POST":
        form = AddUserToUserMadeGroupForm(request.POST, request=request, groupId=groupId)

        if form.is_valid():
            group = UserMadeGroup.objects.filter(id=groupId).first()
            users = form.cleaned_data.get('users')
            current_user = request.user
            for user in users:
                group.members.add(user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect(group.get_absolute_url())
    else:
        form = AddUserToUserMadeGroupForm(request=request, groupId=groupId)
    return render(request, 'add_users_to_group.html', {'form': form})

def send_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message_subject = form.cleaned_data.get('message_subject')
            message_text = form.cleaned_data.get('message_text')
            encrypted = form.cleaned_data.get('encrypted')
            sender = request.user
            receiver = form.cleaned_data.get('receiver')
            time_stamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            if encrypted is True:
                bytes_text = message_text.encode("utf-8").strip()
                encrypted_bytes_text = receiver.key.encrypt(bytes_text)
                new_message = Message.objects.create(message_subject=message_subject, message_text='This message is encrypted. Decrypt to view.', encrypted=encrypted, receiver=receiver, sender=sender, encrypted_message_text = encrypted_bytes_text, time_stamp = time_stamp)

            else:
                new_message = Message.objects.create(message_subject=message_subject, message_text=message_text, encrypted=encrypted, receiver=receiver, sender=sender)

            # redirect, or however you want to get to the main view
            return HttpResponseRedirect(reverse('messages'))
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})

def delete_message(request, messageId):
    Message.objects.filter(id=messageId).delete()

    return HttpResponseRedirect(reverse('messages'))

def decrypt_message(request, messageId):
    url = request.META.get('HTTP_REFERER')
    Message.objects.filter(id=messageId).first().decrypt()

    return HttpResponseRedirect(url)

def delete_report(request):
    if request.method == "POST":
        form = DeleteReportForm(request.POST)
        if form.is_valid():
            report = form.cleaned_data.get('report')
            Report.objects.filter(reportName=report).delete()
            return render(request, 'delete_report.html', {'form': form})
    else:
        form = DeleteReportForm()
    return render(request, 'delete_report.html', {'form': form})

def access_report(request):
    if request.method == "POST":
        form = DeleteReportForm(request.POST)
        if form.is_valid():
            rep = form.cleaned_data.get('report')
            report = Report.objects.filter(reportName=rep).first()
            return HttpResponseRedirect(report.get_absolute_url())
    else:
        form = DeleteReportForm()
    return render(request, 'access_report.html', {'form': form})

def edit_report(request):
    if request.method == "POST":
        form = DeleteReportForm(request.POST)
        if form.is_valid():
            rep = form.cleaned_data.get('report')
            report = Report.objects.filter(reportName=rep).first()
            return HttpResponseRedirect(report.get_absolute_url() + '/edit_report')
    else:
        form = DeleteReportForm()
    return render(request, 'edit_report.html', {'form': form})

def sm_edit_report(request, pk):
    rep = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportForm2(request.POST, instance=rep)
        if form.is_valid():
            form.save()
            return render(request, 'edit_report.html', {'form': form})
    else:
        form = ReportForm2(instance=rep)
    return render(request, 'edit_report.html', {'form': form})

def add_report_to_group(request, groupId):
    groupId=groupId
    if request.method == "POST":
        form = AddReportToGroupForm(request.POST, request=request)
        if form.is_valid():
            group = UserMadeGroup.objects.filter(id=groupId).first()
            rep = form.cleaned_data.get('report')
            report = Report.objects.filter(reportName=rep).first()
            if not report in group.reports.all():
                group.reports.add(report)
            return HttpResponseRedirect(group.get_absolute_url())
    else:
        form = AddReportToGroupForm(request=request)
    return render(request, 'add_report_to_group.html', {'form': form})


def add_comment(request, pk):
    pk=pk
    report = Report.objects.filter(id=pk).first()

    if request.method=="POST":
        if(request.POST.get('rating')):
            print(request.POST.get('rating'))
            current = Rating.objects.filter(userName = request.user).first()
            if current:
                Rating.objects.filter(userName = request.user).update(rating = request.POST.get('rating'))
                rating = Rating.objects.filter(userName = request.user).first()
                if rating not in report.ratings.all():
                    report.ratings.add(rating)
            else:
                new = Rating()
                new.userName = request.user
                new.rating = request.POST.get('rating')
                new.save()
                report.ratings.add(new)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.userName = request.user
            comment.timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            comment.save()
            report.comments.add(comment)
            return HttpResponseRedirect(report.get_absolute_url())

    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


def view_comments(request, pk):
    pk=pk
    report = Report.objects.filter(id=pk).first()

    return render(request, 'view_comments.html', {'report': report})
