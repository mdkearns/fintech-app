import requests
import getpass

usr = input("Username: ")
pwd = getpass.getpass(prompt="Password: ")

login = {'username':usr, 'password':pwd}
r = requests.get('http://127.0.0.1:8000/app/fda_authenticate', params=login)

print(r.text)