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

from finance.models import Transaction, Account, Tag, Category, FinancialGoals
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
    transactions = (
        Transaction.objects.filter(date__year=year)
        .exclude(category__name="income")
        .exclude(category__name="savings")
        .exclude(category__name="investments")
        .exclude(category__name="debts")
    )
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
            "title": f"Total spent in {year}",
            "data": {
                "labels": list(sales_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount (€)",
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
                        "label": "Amount (€)",
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
                        "label": "Amount (€)",
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
                        "label": "Amount (€)",
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

    # drop null values or zero values
    category_dict = {k: v for k, v in category_dict.items() if v is not None and v != 0}

    # sort dict by value
    category_dict = dict(
        sorted(category_dict.items(), key=lambda item: item[1], reverse=True)
    )

    return JsonResponse(
        {
            "title": f"Total spent by category {year}",
            "data": {
                "labels": list(category_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount (€)",
                        "backgroundColor": generate_color_palette(len(category_dict)),
                        "borderColor": generate_color_palette(len(category_dict)),
                        "data": list(category_dict.values()),
                    }
                ],
            },
        }
    )


@staff_member_required
def get_transaction_chart_by_category_per_month(request, year, month):
    categories = Category.objects.all().exclude(name="income")
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

    # sort dict by value
    category_dict = dict(
        sorted(category_dict.items(), key=lambda item: item[1], reverse=True)
    )

    return JsonResponse(
        {
            "title": f"Transactions per Category - {month}/{year}",
            "data": {
                "labels": list(category_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount (€)",
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
                        "label": "Amount (€)",
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
                        "label": "Amount (€)",
                        "backgroundColor": generate_color_palette(len(account_dict)),
                        "borderColor": generate_color_palette(len(account_dict)),
                        "data": list(account_dict.values()),
                    }
                ],
            },
        }
    )


@staff_member_required
def get_average_spent_category_monthly(request, year=2023):
    """Get average spent by category monthly"""
    # get the number of the current month
    current_month = date.today().month
    categories = Category.objects.all()
    category_dict = dict()
    for category in categories:
        total_per_year = (
            Transaction.objects.filter(category=category)
            .filter(date__year=year)
            .aggregate(total=Coalesce(Sum("amount"), Decimal(0)))["total"]
        )
        category_dict[category.name] = (
            total_per_year / current_month if total_per_year else 0
        )

    # drop null values or zero values
    category_dict = {k: v for k, v in category_dict.items() if v is not None and v != 0}

    # sort dict by value
    category_dict = dict(
        sorted(category_dict.items(), key=lambda item: item[1], reverse=True)
    )

    return JsonResponse(
        {
            "title": f"Average spent by category in {year}",
            "data": {
                "labels": list(category_dict.keys()),
                "datasets": [
                    {
                        "label": "Amount (€)",
                        "backgroundColor": generate_color_palette(len(category_dict)),
                        "borderColor": generate_color_palette(len(category_dict)),
                        "data": list(category_dict.values()),
                    }
                ],
            },
        }
    )


@staff_member_required
def get_average_spent_big_category_monthly(request, year=2023):
    """Get average spent by category monthly"""
    # get the number of the current month
    needs = [
        "bills",
        "mobile",
        "bank fee",
        "transportation",
        "phone",
        "commuting",
        "rent",
        "grocery",
        "health",
        "insurance",
        "education",
        "utilities",
    ]
    savings = ["savings", "investments", "debts"]
    total = 0
    current_month = date.today().month

    categories = Category.objects.all().exclude(name="income")
    category_dict = dict()
    for category in categories:
        total_per_year = (
            Transaction.objects.filter(category=category)
            .filter(date__year=year)
            .aggregate(total=Coalesce(Sum("amount"), Decimal(0)))["total"]
        )
        category_dict[category.name] = (
            total_per_year / current_month if total_per_year else 0
        )

    # drop null values or zero values
    category_dict = {k: v for k, v in category_dict.items() if v is not None and v != 0}

    # sort dict by value
    category_dict = dict(
        sorted(category_dict.items(), key=lambda item: item[1], reverse=True)
    )

    # get the total spent in needs, wants and savings
    needs_total = 0
    wants_total = 0
    savings_total = 0
    for category in category_dict:
        if category in needs:
            needs_total += category_dict[category]
        elif category in savings:
            savings_total += category_dict[category]
        else:
            wants_total += category_dict[category]
    total = needs_total + wants_total + savings_total
    return JsonResponse(
        {
            "title": f" Average spent in year {year} - Total spent: €{total}",
            "data": {
                "labels": ["Needs", "Wants", "Savings"],
                "datasets": [
                    {
                        "label": "Amount (€)",
                        "backgroundColor": generate_color_palette(3),
                        "borderColor": generate_color_palette(4),
                        "data": [needs_total, wants_total, savings_total],
                    }
                ],
            },
        }
    )


@staff_member_required
def get_big_category_monthly(request, year, month):
    """Get average spent by category monthly"""
    # get the number of the current month
    needs = [
        "bills",
        "mobile",
        "bank fee",
        "transportation",
        "phone",
        "commuting",
        "rent",
        "grocery",
        "health",
        "insurance",
        "education",
        "utilities",
    ]
    savings = ["savings", "investments", "debts"]

    categories = Category.objects.all().exclude(name="income")
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

    # sort dict by value
    category_dict = dict(
        sorted(category_dict.items(), key=lambda item: item[1], reverse=True)
    )

    # get the total spent in needs, wants and savings
    needs_total = 0
    wants_total = 0
    savings_total = 0
    for category in category_dict:
        if category in needs:
            needs_total += category_dict[category]
        elif category in savings:
            savings_total += category_dict[category]
        else:
            wants_total += category_dict[category]

    return JsonResponse(
        {
            "title": f"Spent in {month} / {year} - Total spent: €{sum(category_dict.values())}",
            "data": {
                "labels": ["Needs", "Wants", "Savings"],
                "datasets": [
                    {
                        "label": "Amount (€)",
                        "backgroundColor": generate_color_palette(3),
                        "borderColor": generate_color_palette(4),
                        "data": [needs_total, wants_total, savings_total],
                    }
                ],
            },
        }
    )


@staff_member_required
def calculate_rule_503020(request, income=4200):
    """Calculate the 50/30/20 rule"""

    needs = income * 0.5
    wants = income * 0.3
    savings = income * 0.2

    return JsonResponse(
        {
            "title": f"Rule 50/30/20 for an income of: €{income}",
            "data": {
                "labels": ["Needs", "Wants", "Savings"],
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": generate_color_palette(5),
                        "borderColor": generate_color_palette(6),
                        "data": [needs, wants, savings],
                    }
                ],
            },
        }
    )


@staff_member_required
def get_financial_goals_chart(request):
    goals = FinancialGoals.objects.all()
    labels = []
    goal_amounts = []
    current_amounts = []

    for goal in goals:
        labels.append(goal.name)
        goal_amounts.append(float(goal.goal_amount))
        current_amounts.append(float(goal.current_amount))

    return JsonResponse(
        {
            "title": "Financial Goals",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Goal Amount (€)",
                        "backgroundColor": "#e5e5e5",
                        "data": goal_amounts,
                    },
                    {
                        "label": "Current Amount (€)",
                        "backgroundColor": "#ffc8dd",
                        "data": current_amounts,
                    },
                ],
            },
            "options": {
                "scales": {
                    "xAxes": [{"stacked": False}],
                    "yAxes": [{"stacked": False}],
                },
                "responsive": True,
                "maintainAspectRatio": False,
            },
        }
    )
