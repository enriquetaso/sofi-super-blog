from django.test import TestCase
import unittest
from unittest import TestCase
from rest_framework.permissions import IsAuthenticated

from .views import TransactionViewSet
from .models import Transaction
from .serializers import TransactionSerializer


class TestTransactionViewSet(TestCase):
    def setUp(self):
        self.queryset = Transaction.objects.all().order_by("date")
        self.serializer_class = TransactionSerializer

    def test_queryset(self):
        self.assertEqual(self.queryset, TransactionViewSet().get_queryset())

    def test_serializer_class(self):
        self.assertEqual(
            self.serializer_class, TransactionViewSet().get_serializer_class()
        )

    def test_permission_classes(self):
        self.assertEqual([IsAuthenticated], TransactionViewSet().get_permissions())


import unittest
from app.models import Transaction
from app.serializers import TransactionSerializer


class TestTransactionSerializer(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction.objects.create(
            account="test_account",
            date="2020-01-01",
            description="test_description",
            place="test_place",
            amount=100,
            tags="test_tags",
            category="test_category",
        )

    def test_serializer(self):
        serializer = TransactionSerializer(instance=self.transaction)

        self.assertEqual(serializer.data["id"], self.transaction.id)
        self.assertEqual(serializer.data["account"], "test_account")
        self.assertEqual(serializer.data["date"], "2020-01-01")
        self.assertEqual(serializer.data["description"], "test_description")
        self.assertEqual(serializer.data["place"], "test_place")
        self.assertEqual(serializer.data["amount"], 100)
        self
