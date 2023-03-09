from django.contrib.admin.apps import AdminConfig


class FinanceAdminConfig(AdminConfig):
    default_site = "mysite.admin.FinanceAdminSite"
