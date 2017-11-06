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
	

req = requests.get('http://127.0.0.1:8000/app/get_reports', params=login)

print()
print("Available reports to view:\n")
print(req.text)