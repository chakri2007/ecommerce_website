from django.urls import path
from . import views

urlpatterns = [
    path('sell/', views.add_selling_object, name='add_selling_object'),
    path('add/', views.add_product_page, name='add_product_page'),
    path('product_list/', views.product_list, name='product_list'),
    
]