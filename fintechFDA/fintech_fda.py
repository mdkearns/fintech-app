import requests

authenticated = False

while not authenticated:

	usr = input("Username: ")
	pwd = input("Password: ")
	login = {'username':usr, 'password':pwd}
	r = requests.get('http://127.0.0.1:8000/app/fda_authenticate', params=login)

	
	if r.text == "You have logged in successfully!":
		authenticated = True
	
	print(r.text)
	

print(r.text)