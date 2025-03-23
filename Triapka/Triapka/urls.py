from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from orders.views import stripe_webhook


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),

    path('orders/', include('orders.urls', namespace='orders')),
    
    path('admin_panel/', include('admin_panel.urls', namespace='admin_panel')),
    path('stripe/webhook/', stripe_webhook, name='stripe_webhook')


] 
if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
