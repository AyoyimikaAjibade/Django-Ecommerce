from django.urls import path
from . import views



app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<str:category_id>/', views.product_list_category, name='product_list_category'),
    path('product_detail/<str:id>/', views.product_detail, name='product_detail'),
    path('review/<str:product_id>', views.review, name='review'),
]
