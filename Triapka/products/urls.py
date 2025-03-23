from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'products'

urlpatterns = [
	path('', views.HomeView.as_view() , name='home'),
    
    path('search/<str:gender>/', views.products_list_view , name='category'),   
    path('item/<int:product_id>/', views.item , name='item'),
    path('basket/add/<int:product_id>/',views.basket_add , name='basket_add'),
    path('basket/remove/<int:basket_id>/', views.basket_remove , name='basket_remove'),
]