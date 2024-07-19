import requests

requests = requests.get('http://127.0.0.1:8000')
print(requests.json())