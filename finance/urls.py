from django.urls import path
from rest_framework.routers import DefaultRouter
from finance import views
from .views import (
    TransactionViewSet,
    AccountViewSet,
    TagViewSet,
    CategoryViewSet,
    TransactionsCVSExportView,
)


router = DefaultRouter()
router.register(r"transactions", TransactionViewSet, basename="transactions")
router.register(r"accounts", AccountViewSet, basename="accounts")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"categories", CategoryViewSet, basename="categories")


urlpatterns = [
    path(
        "transactions/export/",
        TransactionsCVSExportView.as_view(),
        name="transactions-export",
    ),
    path(
        "chart/filter-options/", views.get_filter_options, name="chart-filter-options"
    ),
    path(
        "chart/transactions/<int:year>/",
        views.get_transaction_chart,
        name="chart-transactions",
    ),
    path(
        "chart/transaction-by-categories-per-month/<int:year>/<int:month>/",
        views.get_transaction_chart_by_category_per_month,
        name="chart-transaction-by-categories-per-month",
    ),
    path(
        "chart/transaction-by-categories/<int:year>/",
        views.get_transaction_chart_by_category,
        name="chart-transaction-categories",
    ),
    path(
        "chart/transaction-by-tags/<int:year>/",
        views.get_transaction_chart_by_tag,
        name="chart-transaction-tags",
    ),
    path(
        "chart/transaction-by-accounts/<int:year>/",
        views.get_transaction_chart_by_account,
        name="chart-transaction-accounts",
    ),
    path(
        "chart/get-average-spent-category-monthly/<int:year>/",
        views.get_average_spent_category_monthly,
        name="chart-average-spent-category-monthly",
    ),
    path(
        "chart/get-average-spent-big-category-monthly/<int:year>/",
        views.get_average_spent_big_category_monthly,
        name="chart-average-spent-big-category-monthly",
    ),
    path(
        "chart/get-rule-from-income/<int:income>/",
        views.calculate_rule_503020,
        name="chart-get-rule-from-income",
    ),
    path(
        "chart/get-financial-goals/",
        views.get_financial_goals_chart,
        name="chart-get-financial-goals",
    ),
    path(
        "chart/get-big-category-montly/<int:month>/",
        views.get_big_category_monthly,
        name="chart-get-big-category-montly",
    ),
]
urlpatterns += router.urls
