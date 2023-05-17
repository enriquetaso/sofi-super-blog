from django.contrib.auth.models import User
from rest_framework.test import APILiveServerTestCase
from rest_framework.test import RequestsClient

from finance import models


class BasicAuthRequestClientTestCase(APILiveServerTestCase):
    """Test using the Python library `requests`.

    RequestsClient exposes exactly the same interface as if
    you were using a requests session directly.

    This may be useful if:
    - You are expecting to interface with the API primarily
      from another Python service, and want to test the
      service at the same level as the client will see.
    - You want to write tests in such a way that they can
      also be run against a staging or live environment.
    """

    def setup(self):
        """Set up the test."""
        super().setUp()
        self.client = RequestsClient()

    def test_get_tags_using_basicauth(self):
        """Test that we can get a list of tags using basic auth."""
        client = RequestsClient()
        # Create some tags.
        models.Tag.objects.create(name="tag1")
        models.Tag.objects.create(name="tag2")
        # Create a user.
        password = "demo"
        user = User.objects.create_user(
            username="demo", email="demo@demo.com", password=password
        )

        url = "https://localhost/finance/tags/"
        response = client.get(url, auth=(user.username, password))
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_create_tag_using_basicauth(self):
        """Test that we can create a tag using basic auth."""
        client = RequestsClient()
        password = "demo"
        user = User.objects.create_user(
            username="demo", email="demo@demo.com", password=password
        )

        payload = {"name": "tag3"}
        url = "https://localhost/finance/tags/"
        response = client.post(url, auth=(user.username, password), data=payload)
        assert response.status_code == 201
        assert response.json()["name"] == "tag3"

    def test_create_transaccion(self):
        models.Tag.objects.create(name="tag1")
        models.Tag.objects.create(name="tag2")
        category1 = models.Category.objects.create(name="category1")
        password = "demo"
        user = User.objects.create_user(
            username="demo", email="demo@demo.com", password=password
        )
        account1 = models.Account.objects.create(
            name="account1", owner=user, balance=100
        )

        client = RequestsClient()
        tags_response = client.get(
            "https://localhost/finance/tags/", auth=(user.username, password)
        )
        tags = tags_response.json()

        url_get_category = f"https://localhost/finance/categories/{category1.pk}/"
        categories_response = client.get(
            url_get_category, auth=(user.username, password)
        )
        category = categories_response.json()

        url_get_account = f"https://localhost/finance/accounts/{account1.pk}/"
        account_response = client.get(url_get_account, auth=(user.username, password))
        account = account_response.json()

        payload = {
            "description": "description1",
            "place": "place1",
            "amount": 100,
            "date": "2020-01-01",
            "account": account["id"],
            "category": category,
            "tags": tags,
        }
        url_tran = "https://localhost/finance/transactions/"
        header = {"Content-Type": "application/json"}
        response = client.post(
            url_tran, auth=(user.username, password), json=payload, headers=header
        )
        assert response.status_code == 201
        assert response.json()["description"] == "description1"


class SessionAuthenticationTestCase(APILiveServerTestCase):
    def test_get_tags_with_sessionauthentication(self):
        pass
