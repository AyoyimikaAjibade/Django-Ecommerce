from django.urls import path
from .views import OrderSummaryView, add_to_cart, remove_from_cart, remove_single_product_from_cart, CheckoutView, PaymentView

app_name = 'orders'

urlpatterns = [
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('add_to_cart/<str:id>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<str:id>', remove_from_cart, name='remove_from_cart'),
    path('remove_product_from_cart/<str:id>', remove_single_product_from_cart, name='remove_single_product_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment'),

]