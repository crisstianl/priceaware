"""
priceaware URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', admin.site.urls),
    path('priceaware/', include('web.urls')),
]
