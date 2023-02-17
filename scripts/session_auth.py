import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("DJANGO_USERNAME", "admin")
password = os.getenv("DJANGO_PASSWORD", "admin")


def main():
    """Main function"""

    url = "http://localhost/finance/categories/"
    s = requests.Session()
    s.auth = (username, password)
    response = s.get(url)
    print(response.json())


if __name__ == "__main__":
    main()
