import csv
from datetime import date, timedelta, timezone

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

    def get(self, request, *args, **kwargs) -> HttpResponse:
        # Create the HttpResponse object with the appropriate CSV header.
        # Get transactions from last 90 days

        # TODO: 'WSGIRequest' object has no attribute 'query_params'
        # /finance/transactions/export/?days=30
        days_to_subtract = int(request.GET.get("days", 90))
        today = date.today()
        filter_from_date = today - timedelta(days=days_to_subtract)

        filename = f"transactions_from_{filter_from_date}_to_{today}.csv"
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="' + filename + '"'

        writer = csv.writer(response)
        writer.writerow(["date", "place", "description", "category", "amount", "tags"])

        transactions = Transaction.objects.all().filter(date__gte=filter_from_date)

        for transaction in transactions:
            transactionrow = []
            transactionrow.append(transaction.date.isoformat())
            transactionrow.append(transaction.place)
            transactionrow.append(transaction.description)
            transactionrow.append(transaction.category.name)
            transactionrow.append(transaction.amount)
            for tag in transaction.tags.all():
                transactionrow.append(tag.name)
            writer.writerow(transactionrow)

        return response
