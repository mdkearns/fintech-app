import requests

authenticated = False

while not authenticated:

	print()
	usr = input("Username: ")
	pwd = input("Password: ")
	login = {'username':usr, 'password':pwd}
	r = requests.get('http://127.0.0.1:8000/app/fda_authenticate', params=login)

	if r.text == "You have logged in successfully!":
		authenticated = True
	
	print(r.text)
	
#---- create reports ----#
#r = requests.get('http://127.0.0.1:8000/app/make_reports', params=login)
#print(r.text)
#------------------------#

req = requests.get('http://127.0.0.1:8000/app/get_reports', params=login)

print()
print("Available reports to view:\n")
#print(req.text)

reports = req.text.split(',')

for report in reports:
	print("\t" + str(report))

selection = input("\nEnter the name of the report to view (q to quit): ")

last_report = None

while True:
	
	#validate selected option 
	
	if selection == "s":
		print("\nAvailable reports to view:\n")
		for report in reports:
			print("\t" + str(report))
		selection = input("\nEnter the name of the next report to view (q to quit): ")
	if selection == "d":
		file_to_download = input("\nEnter the name of the file to download: ")
		print("\nDownloaded file \"" + file_to_download + "\" for report: " + last_report)
		selection = input("\nEnter the name of the next report to view (q to quit): ")
	if selection == "q":
		break
		
	last_report = selection
	
	if selection in reports:
		login['report'] = selection
		report_text = requests.get('http://127.0.0.1:8000/app/display_reports', params=login)
		file_text = requests.get('http://127.0.0.1:8000/app/get_report_files', params=login)
		print("\nReport Details:\n")
		print(report_text.text)
		print("\nAttached Files:\n")
		print(file_text.text+ "\n")
		selection = input("Please Enter one of the following:\n\ns : select next report\nd : download files for this report\nq : quit\n\n")
	else:
		print("\nYou selected: ", selection)
		print("This is an invalid command.")
		selection = input("Please Enter one of the following:\n\ns : select next report\nd : download files for this report\nq : quit\n\n")

print("Goodbye.")







