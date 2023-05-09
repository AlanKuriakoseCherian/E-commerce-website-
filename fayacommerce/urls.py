"""fayacommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from store.api import UserViewSet, ProductViewSet, root, user_profile, change_active_status
from store.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProfileView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename="product")
router.register(r'users', UserViewSet, basename="user")


urlpatterns = [
    path('api-doc/', root),
    path('api/', include(router.urls)),
    path('api/user-profile/', user_profile, name="user-profile"),
    path('api/change-active-status/<int:pk>/', change_active_status, name="change-active-status"),

    path('accounts/', include('django.contrib.auth.urls')),
    path('', ProfileView.as_view()),
    path('products', ProductListView.as_view(), name="product-list"),
    path('products/create', ProductCreateView.as_view(), name="product-create"),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name="product-update"),
    path('products/<int:pk>/confirm-delete', ProductDeleteView.as_view(), name="product-delete"),

    path('admin/', admin.site.urls),
]
