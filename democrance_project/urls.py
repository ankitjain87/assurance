"""
URL configuration for democrance_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

# type: ignore[import]
from rest_framework.routers import DefaultRouter
from insurance.views import CustomerViewSet, PolicyViewSet, PolicyListViewSet


router = DefaultRouter()
router.register(r"customer", CustomerViewSet, basename="customer")
router.register(r"quote", PolicyViewSet, basename="quote")
router.register(r"policies", PolicyListViewSet, basename="policy-list")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path(
        "api/v1/customers/search/",
        CustomerViewSet.as_view({"get": "search"}),
        name="customer_search",
    ),
    path(
        "api/v1/policies/<int:policy_id>/history/",
        PolicyListViewSet.as_view({"get": "history"}),
        name="policy_history",
    ),
]
