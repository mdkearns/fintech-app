from tkinter import *
import tkinter.messagebox as message
import requests


class LoginGUI(Frame):

    def __init__(self, m):
	
        self.master = m
	
        super().__init__(self.master)
		
        welcome_message = "Welcome to the File Download Application."
		
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

        self.login_button = Button(self, text="Authenticate", command = self.login)
        self.login_button.grid(columnspan=2)
        self.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
		
        authenticated = False
        login = {'username':username, 'password':password}
        r = requests.get('http://127.0.0.1:8000/app/fda_authenticate', params=login)

        if r.text == "You have logged in successfully!":
            authenticated = True

        if authenticated:
            self.destroy()
            self.signed_in(login)
            message.showinfo("Login info", "Welcome, " + str(username) + "!")
        else:
            message.showerror("Login error", "Invalid Login.")
			
    def signed_in(self, login):
	
        super().__init__(self.master)
		
        welcome_message = "Welcome, " + str(login['username']) + "!"
		
        self.message_label = Label(self, text=welcome_message, justify=CENTER)

        self.message_label.grid(row=1, columnspan=2)

        self.pack()

root = Tk()
fda = LoginGUI(root)
root.mainloop()