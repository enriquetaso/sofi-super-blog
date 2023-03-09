from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path


@staff_member_required
def admin_statistics_view(request):
    return render(request, "admin/statistics.html", {"title": "Statistics"})


class FinanceAdminSite(admin.AdminSite):
    site_header = "enriquetaso.com"
    site_title = "YellowDuck.be"
    index_title = "YellowDuck.be"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list += [
            {
                "name": "Finance Reports",
                "app_label": "my_custom_app",
                "models": [
                    {
                        "name": "Statistics",
                        "object_name": "statistics",
                        "admin_url": "/admin/statistics",
                        "view_only": True,
                    }
                ],
            }
        ]
        return app_list

    def get_urls(self):
        """Overwrite and assigned a URL to our new view. This will be available at /admin/statistics/ o the admin site"""
        urls = super().get_urls()
        my_urls = [
            path(
                "statistics/",
                self.admin_view(self.admin_statistics_view),
                name="statistics",
            ),
        ]
        return my_urls + urls

    def admin_statistics_view(self, request):
        request.current_app = self.name
        return render(request, "admin/statistics.html", {"title": "Statistics"})
