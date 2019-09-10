from django.urls import path
from . import views

# define component namespace
app_name = "web"

# define component url-patterns
urlpatterns = [
    path('', views.index, name='index'),
    path('stores', views.index, name='stores'),
    path('search', views.search, name='search'),
    path('stores/delete', views.delete, name='delete'),
    path('cart', views.cart, name='cart'),
    path('settings', views.settings, name='settings'),
]