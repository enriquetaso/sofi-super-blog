from django.test import TestCase

from rest_framework.permissions import IsAuthenticated

from finance.models import Transaction
from finance.serializers import TransactionSerializer
from finance.views import TransactionViewSet


class TransactionViewSetTestCase(TestCase):
    def setUp(self):
        self.queryset = Transaction.objects.all().order_by("date")
        self.serializer_class = TransactionSerializer

    # def test_queryset(self):
    #     self.assertEqual(self.queryset, TransactionViewSet().all().get_queryset())

    # def test_serializer_class(self):
    #     self.assertEqual(
    #         self.serializer_class, TransactionViewSet().get_serializer_class()
    #     )

    # def test_permission_classes(self):
    #     self.assertEqual([IsAuthenticated()], TransactionViewSet().get_permissions())
