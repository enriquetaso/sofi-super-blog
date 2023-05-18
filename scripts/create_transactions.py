import os

import requests
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("DJANGO_USERNAME", "admin")
password = os.getenv("DJANGO_PASSWORD", "admin")


def get_tags():
    url = "http://localhost/finance/tags/"
    response = requests.get(url, auth=(username, password))
    return response.json()


def create_tag(name):
    url = "http://localhost/finance/tags/"
    payload = {"name": name}
    response = requests.post(url, auth=(username, password), data=payload)
    return response.json()


def get_tag(name):
    url = "http://localhost/finance/tags/"
    response = requests.get(f"{url}{name}/", auth=(username, password))
    return response.json()


def delete_tag(name):
    url = "http://localhost/finance/tags/"
    response = requests.delete(f"{url}{name}/", auth=(username, password))
    print(response.status_code)


def create_category(name):
    url = "http://localhost/finance/categories/"
    payload = {"name": name}
    response = requests.post(url, auth=(username, password), data=payload)
    return response.json()


def get_categories():
    url = "http://localhost/finance/categories/"
    response = requests.get(url, auth=(username, password))
    return response.json()


def get_category(name):
    url = "http://localhost/finance/categories/"
    response = requests.get(f"{url}{name}/", auth=(username, password))
    return response.json()


def delete_category(name):
    url = "http://localhost/finance/categories/"
    response = requests.delete(f"{url}{name}/", auth=(username, password))
    print(response.status_code)


def create_account(name, balance=0, currency="GBP", account_type="bank", owner=1):
    url = "http://localhost/finance/accounts/"
    payload = {
        "name": name,
        "balance": str(balance),
        "owner": owner,
    }
    response = requests.post(url, auth=(username, password), data=payload)
    return response.json()


def get_accounts():
    url = "http://localhost/finance/accounts/"
    response = requests.get(url, auth=(username, password))
    return response.json()


def get_account(name):
    url = "http://localhost/finance/accounts/"
    response = requests.get(f"{url}{name}/", auth=(username, password))
    return response.json()


def delete_account(name):
    url = "http://localhost/finance/accounts/"
    response = requests.delete(f"{url}{name}/", auth=(username, password))
    print(response.status_code)


def get_transactions():
    url = "http://localhost/finance/transactions/"
    response = requests.get(url, auth=(username, password))
    return response.json()


def create_transaction(account, category, tags=None):
    url = "http://localhost/finance/transactions/"
    payload = {
        "account": account,
        "date": "2020-01-01",
        "description": "test",
        "place": "test",
        "amount": 100,
        "tags": tags,
        "category": category,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        url, auth=(username, password), json=payload, headers=headers
    )
    return response.json()


def main():
    # holiday_tag = create_tag("holiday")
    # coffee_category = create_category("coffee")
    # revolut_account = create_account(name="Revolut", balance=114)

    revolut_account = get_account(1)
    tags = get_tags()
    print(tags)
    coffee_category = get_category(3)
    print(coffee_category)
    print(revolut_account)

    # tagl = [tag for tag in tags if tag["name"] == "tag3"]

    create_transaction(account=1, category=coffee_category, tags=tags)

    # pk_to_remove = [tag["id"] for tag in tags if tag["name"] == "tag3"]
    # print(pk_to_remove)
    # for pk in pk_to_remove:
    #     print(pk)
    #     delete_tag(pk)


if __name__ == "__main__":
    main()
