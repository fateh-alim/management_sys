"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from stockmgmt import views as mg_views
from login_auth import views as login_views
from products import views as prod_views
from api import views as API_views
from django.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('products/', API_views.products_list, name='Products_list'),
    path('products/<int:id>', API_views.product_detail, name='Product_detail'),
    path('category/', API_views.category_list, name='Category_list'),
    path('category/<int:id>', API_views.category_detail, name='Category_detail'),

    
    path('', login_views.home, name='home'),
    path('signin/', login_views.signin, name='Signin'),
    path('signup/', login_views.signup, name='Signup'),
    path('signout/', login_views.signout, name='Signout'),
    path('list_products/', prod_views.list_products, name='list_products'),
    path('add_item/', prod_views.add_item, name='add_item'),
    path('add_category/', prod_views.add_category, name='add_category'),
    path('update_item/<str:pk>/', prod_views.update_item, name="update_item"),
    path('delete_item/<str:pk>/', prod_views.delete_item, name="delete_item"),
    path('stock_detail/<str:pk>/', mg_views.stock_detail, name="stock_detail"),
    path('issue_item/<str:pk>/', mg_views.issue_item, name="issue_item"),
    path('receive_item/<str:pk>/', mg_views.receive_item, name="receive_item"),
    path('reorder_level/<str:pk>/', prod_views.reorder_level, name="reorder_level"),
    path('account/', include('registration.backends.default.urls')),
    path('list_history/', mg_views.list_history, name='list_history'),
    path('admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)