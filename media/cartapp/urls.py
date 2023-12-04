from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('remove/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),  
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    
   

]