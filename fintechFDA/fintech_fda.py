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

while True:
	
	#validate selected option 
	
	if selection == "q":
		break
	
	if selection in reports:
		login['report'] = selection
		report_text = requests.get('http://127.0.0.1:8000/app/display_reports', params=login)
		print()
		print(report_text.text)
		selection = input("Enter the name of the next report to view (q to quit): ")
	else:
		print("\nYou selected: ", selection)
		print("This report does not exist.")
		selection = input("Specify the name of a valid report from the list above (q to quit): ")

print("Goodbye.")