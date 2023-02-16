import requests
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("DJANGO_USERNAME", "admin")
password = os.getenv("DJANGO_PASSWORD", "admin")
url = "http://localhost/api-auth/login/"
# url = 'http://localhost/api-auth/login/?next=/finance/transactions/'

session = requests.Session()
response = session.get(url, data={"username": username, "password": password})

cookies = requests.utils.dict_from_cookiejar(session.cookies)

headers = {"Accept": "application/json", "X-CSRF-Token": cookies["csrftoken"]}
response = session.post(url, headers=headers)
print(response.status_code)
print(response.cookies)
print(response.text)
