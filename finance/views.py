import csv
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth, Coalesce
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import viewsets

from finance.models import Transaction, Account, Tag, Category
from finance.serializers import (
    TransactionSerializer,
    AccountSerializer,
    TagSerializer,
    CategorySerializer,
)
from finance.utils.charts import (
    months,
    colorPrimary,
    colorSuccess,
    colorDanger,
    generate_color_palette,
    get_year_dict,
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


@staff_member_required
def get_filter_options(request):
    grouped_purchases = (
        Transaction.objects.annotate(year=ExtractYear("date"))
        .values("year")
        .order_by("-year")
        .distinct()
    )
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse(
        {
            "options": options,
        }
    )


@staff_member_required
def get_transaction_chart(request, year):
    transactions = Transaction.objects.filter(date__year=year)
    group_by_month = (
        transactions.annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(total=Coalesce(Sum("amount"), Decimal(0)))
        .values("month", "total")
        .order_by("month")
    )

    sales_dict = get_year_dict()

    for group in group_by_month:
        sales_dict[months[group["month"] - 1]] = round(group["total"], 2)

    return JsonResponse(
        {
            "title": f"Transactions in {year}",
            "data": {
                "labels": list(sales_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": colorPrimary,
                        "borderColor": colorPrimary,
                        "data": list(sales_dict.values()),
                    }
                ],
            },
        }
    )


@staff_member_required
def get_account_chart(request, year):
    accounts = Account.objects.all()
    account_dict = dict()
    for account in accounts:
        account_dict[account.name] = account.transactions.filter(
            date__year=year
        ).aggregate(total=Sum("amount"))["total"]

    return JsonResponse(
        {
            "title": f"Accounts in {year}",
            "data": {
                "labels": list(account_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": generate_color_palette(len(account_dict)),
                        "borderColor": generate_color_palette(len(account_dict)),
                        "data": list(account_dict.values()),
                    }
                ],
            },
        }
    )


@staff_member_required
def get_tag_chart(request, year):
    tags = Tag.objects.all()
    tag_dict = dict()
    for tag in tags:
        tag_dict[tag.name] = tag.transactions.filter(date__year=year).aggregate(
            total=Sum("amount")
        )["total"]

    return JsonResponse(
        {
            "title": f"Tags in {year}",
            "data": {
                "labels": list(tag_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": generate_color_palette(len(tag_dict)),
                        "borderColor": generate_color_palette(len(tag_dict)),
                        "data": list(tag_dict.values()),
                    }
                ],
            },
        }
    )


@staff_member_required
def get_category_chart(request, year):
    categories = Category.objects.all()
    category_dict = dict()
    for category in categories:
        category_dict[category.name] = (
            Transaction.objects.filter(category=category)
            .filter(date__year=year)
            .aggregate(total=Coalesce(Sum("amount"), Decimal(0)))["total"]
        )

    return JsonResponse(
        {
            "title": f"Categories in {year}",
            "data": {
                "labels": list(category_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": generate_color_palette(len(category_dict)),
                        "borderColor": generate_color_palette(len(category_dict)),
                        "data": list(category_dict.values()),
                    }
                ],
            },
        }
    )


@staff_member_required
def get_transaction_chart_by_category(request, year):
    categories = Category.objects.all()
    category_dict = dict()
    for category in categories:
        category_dict[category.name] = (
            Transaction.objects.filter(category=category)
            .filter(date__year=year)
            .aggregate(total=Coalesce(Sum("amount"), Decimal(0)))["total"]
        )

    return JsonResponse(
        {
            "title": f"Total spent by category {year}",
            "data": {
                "labels": list(category_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": generate_color_palette(len(category_dict)),
                        "borderColor": generate_color_palette(len(category_dict)),
                        "data": list(category_dict.values()),
                    }
                ],
            },
        }
    )

@staff_member_required
def get_transaction_chart_by_category_per_month(request, month):
    year = 2023
    categories = Category.objects.all()
    category_dict = dict()
    for category in categories:
        category_dict[category.name] = (
            Transaction.objects.filter(category=category)
            .filter(date__year=year)
            .filter(date__month=month)
            .aggregate(total=Coalesce(Sum("amount"), Decimal(0)))["total"]

        )
    # drop null values or zero values
    category_dict = {k: v for k, v in category_dict.items() if v is not None and v != 0}

    return JsonResponse(
        {
            "title": f"Transactions per Category - {month}/{year}",
            "data": {
                "labels": list(category_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": generate_color_palette(len(category_dict)),
                        "borderColor": generate_color_palette(len(category_dict)),
                        "data": list(category_dict.values()),
                    }
                ],
            },
        }
    )

@staff_member_required
def get_transaction_chart_by_tag(request, year):
    tags = Tag.objects.all()
    tag_dict = dict()
    for tag in tags:
        tag_dict[tag.name] = (
            Transaction.objects.filter(tags=tag)
            .filter(date__year=year)
            .aggregate(total=Coalesce(Sum("amount"), Decimal(0)))["total"]
        )

    return JsonResponse(
        {
            "title": f"Total spent by tag in {year}",
            "data": {
                "labels": list(tag_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": generate_color_palette(len(tag_dict)),
                        "borderColor": generate_color_palette(len(tag_dict)),
                        "data": list(tag_dict.values()),
                    }
                ],
            },
        }
    )


@staff_member_required
def get_transaction_chart_by_account(request, year):
    accounts = Account.objects.all()
    account_dict = dict()
    for account in accounts:
        account_dict[account.name] = (
            Transaction.objects.filter(account=account)
            .filter(date__year=year)
            .aggregate(total=Coalesce(Sum("amount"), Decimal(0)))["total"]
        )

    return JsonResponse(
        {
            "title": f"Account Usage in {year}",
            "data": {
                "labels": list(account_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": generate_color_palette(len(account_dict)),
                        "borderColor": generate_color_palette(len(account_dict)),
                        "data": list(account_dict.values()),
                    }
                ],
            },
        }
    )
