from django.urls import path
from rest_framework.routers import DefaultRouter
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
]
urlpatterns += router.urls
