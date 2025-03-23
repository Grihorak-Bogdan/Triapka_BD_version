from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'admin_panel'

urlpatterns = [
	path('admin_products/', views.AdminProducts.as_view() , name='admin_products'),
    path('admin_orders/', views.AdminOrders.as_view() , name='admin_orders'),
    path('admin_brands/', views.AdminBrands.as_view() , name='admin_brands'),
    path('form_add_products/', views.FormAddProducts.as_view() , name='form_add_products'),
     path('form_add_brands/', views.FormAddBrands.as_view() , name='form_add_brands'),
   	path('edit_product/<int:pk>/', views.FormEditProducts.as_view(), name='form_edit_products'),
]