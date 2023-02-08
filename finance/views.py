import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from finance.models import Transaction, Account, Tag, Category
from finance.serializers import (
    TransactionSerializer,
    AccountSerializer,
    TagSerializer,
    CategorySerializer,
)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("date")
    serializer_class = TransactionSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionsCVSExportView(View):
    """Class based view to export transactions to CSV

    Regular Django View is use to it's easier to response a HttpResponse object.
    """

    def get(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow(["date", "description", "place", "amount", "tags", "category"])

        transactions = Transaction.objects.all().values_list(
            "date", "description", "place", "amount", "tags", "category"
        )
        for transaction in transactions:
            writer.writerow(transaction)

        return response
