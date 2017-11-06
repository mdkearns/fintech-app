import requests

r = requests.get('http://127.0.0.1:8000/app/fda_authenticate')

print(r.text)