from django.test import TestCase

from finance.models import Transaction
from finance.serializers import TransactionSerializer


# class TestTransactionSerializer(TestCase):
# def setUp(self):
#     self.transaction = Transaction.objects.create(
#         account="test_account",
#         date="2020-01-01",
#         description="test_description",
#         place="test_place",
#         amount=100,
#         tags="test_tags",
#         category="test_category",
#     )

# def test_serializer(self):
#     serializer = TransactionSerializer(instance=self.transaction)

#     self.assertEqual(serializer.data["id"], self.transaction.id)
#     self.assertEqual(serializer.data["account"], "test_account")
#     self.assertEqual(serializer.data["date"], "2020-01-01")
#     self.assertEqual(serializer.data["description"], "test_description")
#     self.assertEqual(serializer.data["place"], "test_place")
#     self.assertEqual(serializer.data["amount"], 100)
