from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import RequestsClient


class RequestClientTestCase(TestCase):
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
        client = RequestsClient()
        response = client.get("http://testserver/users/")
        assert response.status_code == 200
