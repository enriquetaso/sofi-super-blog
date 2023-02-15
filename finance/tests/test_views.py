import json
from rest_framework import status
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from finance import models
from finance import serializers


class BaseTestCase(TestCase):
    def setUp(self):
        password = "password"
        self.adminuser = User.objects.create_superuser(
            "myuser", "myemail@test.com", password
        )
        self.account = models.Account.objects.create(
            name="test_account", balance=1000, owner=self.adminuser
        )

        self.tag = models.Tag.objects.create(name="test_tag")
        self.tag2 = models.Tag.objects.create(name="test_tag2")
        self.category = models.Category.objects.create(name="test_category")

        self.transaction1 = models.Transaction.objects.create(
            account=self.account,
            date="2020-01-01",
            description="test_description",
            place="test_place",
            amount=100,
            category=self.category,
        )
        self.transaction1.tags.add(self.tag)

        self.transaction2 = models.Transaction.objects.create(
            account=self.account,
            date="2020-01-01",
            description="test_description",
            place="test_place",
            amount=100,
            category=self.category,
        )
        self.transaction2.tags.add(self.tag)

        # initialize the APIClient app
        self.client = APIClient()
        self.client.login(username=self.adminuser.username, password=password)


class TransaccionsViewTest(BaseTestCase):
    def test_get_all_transactions(self):
        """Get all transactions."""
        # get API response
        response = self.client.get("/finance/transactions/", format="json")
        # get data from db
        transactions = models.Transaction.objects.all()
        serializer = serializers.TransactionSerializer(transactions, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_transaction(self):
        """Get valid single transaction."""
        url = f"/finance/transactions/{self.transaction1.pk}/"
        response = self.client.get(url, format="json")

        transaction = models.Transaction.objects.get(pk=self.transaction1.pk)
        serializer = serializers.TransactionSerializer(transaction)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_transaction(self):
        """Get invalid single transaction."""
        url = f"/finance/transactions/999/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_transaction(self):
        """Create valid transaction."""
        valid_payload = {
            "account": self.account.pk,
            "date": "2020-01-01",
            "description": "test_description",
            "place": "test_place",
            "amount": 100,
            "tags": [
                serializers.TagSerializer(self.tag).data,
                serializers.TagSerializer(self.tag2).data,
            ],
            "category": serializers.CategorySerializer(self.category).data,
        }
        response = self.client.post(
            "/finance/transactions/",
            data=valid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_transaction(self):
        """Create invalid transaction."""
        invalid_payload = {
            "account": self.account.pk,
            "date": "2020-01-01",
            "description": "test_description",
            "place": "test_place",
            "amount": 100,
            "tags": [1, 2, 3],
            "category": self.category.pk,
        }
        response = self.client.post(
            "/finance/transactions/",
            data=json.dumps(invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_transaction(self):
        """Update valid transaction."""
        old_amount = models.Transaction.objects.get(pk=self.transaction1.pk).amount
        valid_payload = {
            "account": self.account.pk,
            "date": "2020-01-01",
            "description": "test_description",
            "place": "test_place",
            "amount": 800,
            "tags": [
                serializers.TagSerializer(self.tag).data,
                serializers.TagSerializer(self.tag2).data,
            ],
            "category": serializers.CategorySerializer(self.category).data,
        }
        url = f"/finance/transactions/{self.transaction1.pk}/"
        response = self.client.put(
            url,
            data=valid_payload,
            format="json",
        )
        new_amount = int(float(response.data["amount"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_amount, valid_payload["amount"])
        self.assertNotEqual(old_amount, new_amount)

    def test_update_invalid_transaction(self):
        """Update invalid transaction."""
        invalid_payload = {
            "account": self.account.pk,
            "date": "2020-01-01",
            "description": "test_description",
            "place": "test_place",
            "amount": 100,
            "tags": [1, 2, 3],
            "category": self.category.pk,
        }
        url = f"/finance/transactions/{self.transaction1.pk}/"
        response = self.client.put(
            url,
            data=json.dumps(invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_transaction(self):
        """Delete valid transaction."""
        url = f"/finance/transactions/{self.transaction1.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_transaction(self):
        """Delete invalid transaction."""
        url = f"/finance/transactions/999/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TagViewTest(BaseTestCase):
    def test_get_all_tags(self):
        """Get all tags."""
        # get API response
        response = self.client.get("/finance/tags/", format="json")
        # get data from db
        tags = models.Tag.objects.all()
        serializer = serializers.TagSerializer(tags, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_tag(self):
        """Create valid tag."""
        valid_payload = {
            "name": "test_tag",
        }
        response = self.client.post(
            "/finance/tags/",
            data=valid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
