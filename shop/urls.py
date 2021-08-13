"""shop URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles .urls import static
from django.urls import path, include

from product.views import (test_view, products_list,
                           ProductsListView, ProductDetailsView, CreateProductView, UpdateProductView,
                           DeleteProductView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', test_view),
    path('api/v1/products/', ProductsListView.as_view()),
    path('api/v1/products/<int:pk>/', ProductDetailsView.as_view()),
    path('api/v1/products/create/', CreateProductView.as_view()),
    path('api/v1/products/update/<int:pk>/', UpdateProductView.as_view()),
    path('api/v1/products/delete/<int:pk>/', DeleteProductView.as_view()),
    path('api/v1/', include('account.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


