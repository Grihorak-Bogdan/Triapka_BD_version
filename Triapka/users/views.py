from django.shortcuts import render , HttpResponseRedirect
from users.forms import UserLoginForm , UserRegistrationForm , UserProfileForm
from django.contrib import auth , messages
from django.urls import reverse , reverse_lazy
from products.models import Basket , ProductCategory , Products
from users.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView , UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.db.models import Sum , F
from django.shortcuts import get_object_or_404


#Profile
class UserProfileView(UpdateView):
    model = User 
    form_class = UserProfileForm
    template_name = 'users/konto.html'
    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)


    def get_success_url(self):
        return reverse_lazy('users:konto', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView , self).get_context_data()
        context['baskets'] =  Basket.objects.filter(user=self.request.user).order_by('-id')  # Преобразуем в список и переворачиваем его

        context['products'] = Products.objects.all()
        context['categories'] = ProductCategory.objects.all() 
        context['unique_genders'] = Products.GenderChoices.choices
        return context

#Ustawienia
class UserUstawieniaView(UpdateView):
    model = User 
    form_class = UserProfileForm
    template_name = 'users/ustawienia.html'
    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)


    def get_success_url(self):
        return reverse_lazy('users:ustawienia', args=(self.object.username,))

    def get_context_data(self, **kwargs):
        context = super(UserUstawieniaView , self).get_context_data()
        context['unique_genders'] = Products.GenderChoices.choices
        return context

#Login
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse('products:home')

#Register
class UserRegistrationView(SuccessMessageMixin , CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Witam'

#Logout
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:home'))


#Calculate for "update_quantity"
def calculate_total_sum(user):
    # Получаем все товары в корзине пользователя
    items = Basket.objects.filter(user=user)
    
    # Считаем общую стоимость: сумму произведений количества на цену для каждого товара
    total_sum = items.aggregate(total=Sum(F('quantity') * F('price')))['total']
    
    # Если в корзине нет товаров, устанавливаем общую стоимость в ноль
    if total_sum is None:
        total_sum = 0
    
    return total_sum


#Update quantity
@require_POST
@csrf_exempt
def update_quantity(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    size = data.get('size')

    if not product_id or quantity is None or size is None:
        return JsonResponse({'success': False, 'message': 'Необходимы product_id, quantity и size'}, status=400)

    try:
        basket_items = Basket.objects.filter(product_id=product_id, size=size, user=request.user)
        if not basket_items.exists():
            return JsonResponse({'success': False, 'message': 'Товар в корзине не найден'}, status=404)

        for basket_item in basket_items:
            basket_item.quantity = quantity  # Заменяем на новое значение
            basket_item.save()

        new_total_quantity = Basket.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum'] or 0
        new_total_sum = Basket.objects.filter(user=request.user).aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
        return JsonResponse({'success': True, 'message': 'Количество обновлено', 'new_total_quantity': new_total_quantity, 'new_total_sum': new_total_sum})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Ошибка: {str(e)}'}, status=500)


class UlubioneListView(ListView):
    model = Products
    template_name = 'users/ulubione.html'
    context_object_name = 'ulubione'

    def get_queryset(self):
        # Получаем queryset избранных продуктов текущего пользователя
        return self.request.user.ulubione.all()
    
    def get_context_data(self, **kwargs):
        context = super(UlubioneListView , self).get_context_data()
        context['unique_genders'] = Products.GenderChoices.choices
        return context

# def register(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data = request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Witam')
#             return HttpResponseRedirect(reverse('users:login'))   
#     else:
#         form = UserRegistrationForm()
#     return render(request , '', {
#         "form" : form ,
#     })


# @login_required
# def konto(request ):
#     baskets = Basket.objects.filter(user=request.user)   

#     total_sum = sum(basket.sum() for basket in baskets )
#     total_quantity = sum(basket.quantity for basket in baskets )


#     if request.method == "POST" :
#         form = UserProfileForm( instance=request.user , data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('products:konto'))
#     else:
#         form = UserProfileForm(instance=request.user)
        

#     return render(request , 'users/konto.html' , {
#         "total_quantity" : total_quantity,
#         "total_sum" : total_sum,
#         "baskets" : baskets ,
#         "form" : form ,
#         "products" : Products.objects.all(),
#         "categories" : ProductCategory.objects.all(),
#         "unique_genders": Products.objects.values_list('gender', flat=True).distinct() ,
#     })