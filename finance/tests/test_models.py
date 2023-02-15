from django.test import TestCase
from django.contrib.auth.models import User
from finance import models


class BaseTestCase(TestCase):
    """Base test case."""

    def setUp(self):
        """Set up test data."""
        self.adminuser = User.objects.create_superuser(
            "myuser", "myemail@test.com", "password"
        )

        self.account = models.Account.objects.create(
            name="Bank Account A", balance=1000, owner=self.adminuser
        )

        self.tag = models.Tag.objects.create(name="test_tag")
        self.category = models.Category.objects.create(name="test_category")

        self.transaction = models.Transaction.objects.create(
            account=self.account,
            date="2020-01-01",
            description="test_description",
            place="test_place",
            amount=100,
            category=self.category,
        )
        self.transaction.tags.add(self.tag)


class AccountTestCase(BaseTestCase):
    """Test Account model."""

    def test_account_str(self):
        """Test Account model string representation."""
        self.assertEqual(str(self.account), "Bank Account A")


class TransactionTestCase(BaseTestCase):
    """Test Transaction model."""

    def test_transaction_str(self):
        """Test Transaction model string representation."""
        self.assertEqual(str(self.transaction), "test_description")

    def test_transaction_tags(self):
        """Test Transaction model tags."""
        self.assertEqual(self.transaction.tags.first(), self.tag)

    def test_transaction_category(self):
        """Test Transaction model category."""
        self.assertEqual(self.transaction.category, self.category)
