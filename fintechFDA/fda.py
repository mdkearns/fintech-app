from tkinter import *
from functools import partial
import tkinter.messagebox as message
import requests


class LoginGUI(Frame):

    def __init__(self, m):
	
        self.master = m
	
        super().__init__(self.master)
		
        welcome_message = "\nWelcome to the File Download Application.\n\n"
		
        self.message_label = Label(self, text=welcome_message, justify=CENTER)
        self.username_label = Label(self, text="Username")
        self.password_label = Label(self, text="Password")

        self.username_entry = Entry(self)
        self.password_entry = Entry(self, show="*")

        self.message_label.grid(row=1, columnspan=2)
        self.username_label.grid(row=2, sticky=E)
        self.password_label.grid(row=3, sticky=E)
        self.username_entry.grid(row=2, column=1)
        self.password_entry.grid(row=3, column=1)
		
        self.space = Label(self, text="\n", justify=CENTER)
        self.space.grid(row=4)
		
        self.pack()

        self.login_button = Button(self, text="Authenticate", command = self.login)
        self.login_button.grid(columnspan=2)
		
        self.space = Label(self, text="\n", justify=CENTER)
        self.space.grid(row=6)
		
        self.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
		
        authenticated = False
        self.login = {'username':username, 'password':password}
        r = requests.get('http://127.0.0.1:8000/app/fda_authenticate', params=self.login)

        if r.text == "You have logged in successfully!":
            authenticated = True

        if authenticated:
            self.destroy()
            self.signed_in(self.login)
        else:
            message.showerror("Login error", "Invalid Login.")
			
    def signed_in(self, login):
	
        req = requests.get('http://127.0.0.1:8000/app/get_reports', params=self.login)

        reports = req.text.split(',')

        print(reports)

        super().__init__(self.master)
		
        welcome_message = "\nWelcome, " + str(login['username']) + "!\n"

        if reports[0] != '':
            reports_message = "The following reports are available for viewing:\n"
            self.message_label = Label(self, text=welcome_message, justify=CENTER)
            self.reports_label = Label(self, text=reports_message, justify=CENTER)
            self.message_label.grid(columnspan=2)
            self.reports_label.grid(columnspan=2)
		
            self.pack()
            r = 2
			
            for report in reports:
                self.report_label = Label(self, text=report, justify=CENTER)
                self.report_label.grid(row=r, sticky=E)
                self.report_select = Button(self, text="View " + report, command = lambda: self.view_report(report))
                self.report_select.grid(row=r, column=1)
                r += 1
                self.pack()
			
            self.space = Label(self, text="\n", justify=CENTER)
            self.space.grid(row=4)
		
            self.pack()
        else:
            reports_message = "You have no available reports to view."
		
            self.message_label = Label(self, text=welcome_message, justify=CENTER)
            self.reports_label = Label(self, text=reports_message, justify=CENTER)
            self.message_label.grid(columnspan=2)
            self.reports_label.grid(columnspan=2)
		
            self.pack()
			
		
    def view_report(self, report_name):
	    self.destroy()
	    super().__init__(self.master)
		
	    self.login['report'] = report_name
	    print(report_name)
		
	    report_text = requests.get('http://127.0.0.1:8000/app/display_reports', params=self.login)
	    
	    self.details_label = Label(self, text="\nReport Details:\n\n"+report_text.text+"\n")
	    self.details_label.grid(column=0)
		
	    self.pack()
	    self.files_label = Label(self, text="\nAttached Files:\n")
	    self.files_label.grid(column=0)
	    self.pack()
		
root = Tk()
fda = LoginGUI(root)
root.mainloop()