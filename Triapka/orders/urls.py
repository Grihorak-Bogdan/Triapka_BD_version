from django.urls import path
from django.contrib.auth.decorators import login_required
from orders.views import OrderCreateView ,CanceledTemplateView, SuccessTemplateView , OrderView
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
    path('orders/<slug:username>/', login_required(views.OrderListView.as_view()) , name='orders'),
    path('order/<int:order_id>/', login_required(OrderView.as_view()), name='order_info'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)