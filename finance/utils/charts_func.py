from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.http import JsonResponse

from finance.models import Category
from finance.models import Transaction
from finance.utils.charts import generate_color_palette


def get_data_category_per_month(request):

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
