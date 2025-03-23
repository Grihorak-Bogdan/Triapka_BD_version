
from django.views.decorators.http import require_POST
import json
import stripe
from django.views.generic.edit import CreateView 
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from http import HTTPStatus

from django.urls import reverse_lazy, reverse
from django.conf import settings

from products.models import Basket , Products
from orders.models import Order
from orders.forms import OrderForm

stripe.api_key = 'sk_test_51PCR72RwB5EeqtbdvTidFbIJcXsUXs8ZRSqMtONBHRcaP41wKdQ4Cd53IBXNeASTECniUEZoNuqkixsaLNA3b4e700gEmrDpyl'

class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'

    def get_context_data(self, **kwargs):
        context = super(SuccessTemplateView , self).get_context_data()
        context['products_new_colection'] = Products.objects.all().order_by('-id')[:6]
        context['unique_genders'] = Products.GenderChoices.choices
        return context

class CanceledTemplateView(TemplateView):
    template_name = 'orders/cancled.html'

class OrderCreateView(CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(OrderCreateView , self).get_context_data()
        context['products_new_colection'] = Products.objects.all().order_by('-id')[:6]
        context['unique_genders'] = Products.GenderChoices.choices
        return context

class OrderListView(ListView):
    model = Order  
    template_name = 'orders/orders.html'
    context_object_name = 'orders' 

    def get_queryset(self):
        
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(initiator=user, status=Order.PAID)
        else:
            return Order.objects.none()  

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        
        context['products_new_collection'] = Products.objects.all().order_by('-id')[:6]
        context['unique_genders'] = Products.GenderChoices.choices
        return context

@method_decorator(login_required, name='dispatch')
class OrderView(TemplateView):
    template_name = 'orders/order.html'
    
    def get_context_data(self, **kwargs):
        context = super(OrderView , self).get_context_data()
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(id=order_id)  # Получаем заказ по ID
        context['order'] = order
        context['products_new_colection'] = Products.objects.all().order_by('-id')[:6]
        context['unique_genders'] = Products.GenderChoices.choices
        return context



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:

        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        fulfill_order(session)

    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()