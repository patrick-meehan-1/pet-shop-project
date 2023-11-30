from django.urls import path
from . import views
from .views import ProductCreateView, add_review

app_name = 'shop'
urlpatterns = [
 path('new_review/<uuid:pk>/', add_review, name='add_review'),
 path('', views.prod_list, name = 'all_products'),
 path('<uuid:category_id>/', views.prod_list, name = 'products_by_category'),
 path('<uuid:category_id>/<uuid:product_id>/', views.product_detail, name = 'product_detail'),
 path('new/', ProductCreateView.as_view(), name='product_create'),
] 