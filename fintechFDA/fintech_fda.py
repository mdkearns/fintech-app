import requests
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfile
import getpass

authenticated = False

while not authenticated:

	print()
	usr = input("Username: ")
	pwd = getpass.getpass("Password: ")
	login = {'username':usr, 'password':pwd}
	r = requests.get('http://127.0.0.1:8000/app/fda_authenticate', params=login)

	if r.text == "You have logged in successfully!":
		authenticated = True
	
	print("\n" + r.text)

req = requests.get('http://127.0.0.1:8000/app/get_reports', params=login)

print()

reports = req.text.split(',')

if reports[0] == '':

	print("\tThere are no available reports to view.")
	
else:

	print("Available reports to view:\n")

	for report in reports:
		print("\t" + str(report))

selection = input("\nEnter the name of the report to view (q to quit): ")

last_report = None

while True:
	 
	# select next report to view
	if selection == "s":
	
		print("\nAvailable reports to view:\n")
		for report in reports:
			print("\t" + str(report))
		selection = input("\nEnter the name of the next report to view (q to quit): ")
	
	# upload file to the report selected
	if selection == "a":
	
		root = tk.Tk()
		root.withdraw()
		dirname = askopenfilename()
		
		with open(dirname, "r") as f:
			file_contents = f.read()
			
		dirname = input("Name the file: ")
		
		login['file'] = file_contents
		login['dirname'] = dirname
		
		response = requests.get('http://127.0.0.1:8000/app/upload_file/', params=login)
		
		print("\nThe file " + dirname + " was added successfully.")
		
		print("\nAvailable reports to view:\n")
		for report in reports:
			print("\t" + str(report))
		selection = input("\nEnter the name of the next report to view (q to quit): ")

	# download file for the report selected
	if selection == "d":
		file_to_download = input("\nEnter the name of the file to download: ")
		login['file'] = file_to_download
		file_returned = requests.get('http://127.0.0.1:8000/app/download_file/', params=login)
		file_to_save = file_returned.text
		
		if file_to_save != "Error.":
			root = tk.Tk()
			root.withdraw()
			f = asksaveasfile(mode='w', defaultextension=".txt")
			f.write(file_to_save)
			f.close()
			print("\nDownloaded file \"" + file_to_download + "\" for report: " + last_report)
		else:
			print("\nInvalid File Name.")
			
		print("\nAvailable reports to view:\n")
		for report in reports:
			print("\t" + str(report))
		selection = input("\nEnter the name of the next report to view (q to quit): ")
	
	# exit the application
	if selection == "q":
		break
		
	last_report = selection
	
	if selection in reports:
		login['report'] = selection
		report_text = requests.get('http://127.0.0.1:8000/app/display_reports', params=login)
		file_text = requests.get('http://127.0.0.1:8000/app/get_report_files', params=login)
		print("\nReport Details:\n")
		print(report_text.text)
		print("Attached Files:\n")
		print(file_text.text+ "\n")
		selection = input("Please enter one of the following:\n\ns : select next report\na : add file to report\nd : download files for this report\nq : quit\n\n")
	else:
		print("\nYou selected: ", selection)
		print("This is an invalid command.")
		selection = input("Please enter one of the following:\n\ns : select next report\na : add file to report\nd : download files for this report\nq : quit\n\n")

print("\nGoodbye.")







