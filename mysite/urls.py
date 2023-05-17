from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("finance/", include("finance.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
