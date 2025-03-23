from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render , HttpResponseRedirect
from products.models import ProductCategory , Products  , Basket , ProductImage , Size , ProductSize
from users.models import User
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import redirect
from django.db.models import Q

from django.core.paginator import Paginator

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods   

# Create your views here.

class HomeView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView , self).get_context_data()
        context['products'] = Products.objects.all()
        context['products_new_colection'] = Products.objects.all().order_by('-id')[:6]
        context['unique_genders'] = Products.GenderChoices.choices
        context['categories'] = ProductCategory.objects.all()
        return context

# class ProductsListView(ListView):
#     model = Products
#     template_name = 'products/search.html'
#     paginate_by = 6 

#     def get_queryset(self):
#         queryset = super(ProductsListView, self).get_queryset()
#         gender = self.kwargs.get('gender')
        
#         return queryset.filter(gender=gender)

#     def get_context_data(self, **kwargs):
#         context = super(ProductsListView , self).get_context_data()
#         gender = self.kwargs.get('gender')
#         context['products'] = Products.objects.all()
#         context['categories'] = ProductCategory.objects.all()
#         context['unique_genders'] = Products.objects.values_list('gender', flat=True).distinct()
#         context['gender'] = gender
#         return context


def products_list_view(request, gender):

   
    products = Products.objects.filter(gender=gender).order_by('-id')
    
    price_ranges = request.GET.getlist('price_ranges')

    sizes = Size.objects.all() 

    if price_ranges:
        query = Q()
        for price_range in price_ranges:
            min_price, max_price = map(int, price_range.split('-'))
            query |= Q(price__gte=min_price, price__lte=max_price)
        products = products.filter(query)

    brands_ranges = request.GET.getlist('brands_ranges')
    if brands_ranges:
        products = products.filter(brands__name__in=brands_ranges)

    categorys_ranges = request.GET.getlist('categorys_ranges')
    if categorys_ranges:
        products = products.filter(category__name__in=categorys_ranges)

    size_ranges = request.GET.getlist('size_ranges')
    if size_ranges :
        products = products.filter(product_in_productsize__size__size__in=size_ranges).distinct()

    paginator = Paginator(products, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    categories = ProductCategory.objects.all()
    unique_genders = Products.GenderChoices.choices
    

    context = {
        'products': products,
        'page_obj': page_obj, 
        'categories': categories,
        'unique_genders': unique_genders,
        'gender': gender ,
        'price_ranges': price_ranges,
        'brands_ranges' : brands_ranges,
        'categorys_ranges' : categorys_ranges,
        'size_ranges': size_ranges,
        'sizes': sizes ,
        "photo_products" : ProductImage.objects.all(),
    }

    return render(request, 'products/search.html', context)
 


def item(request, product_id):
    products = Products.objects.get(id=product_id)
    sizes = Size.objects.all()

    
    if request.method == "POST":
        if request.user.is_authenticated:
            action = request.POST.get('follow', None)
            if action == "unfollow":
                request.user.ulubione.remove(products)
            elif action == "follow":
                request.user.ulubione.add(products)
            request.user.save()
            
            
        else:
            # Redirect to the login page if the user is not authenticated
            return redirect('users:login') # Redirect to a specific view after updating

    return render(request, 'products/item.html', {
        "unique_genders": Products.GenderChoices.choices,
        "products": products,
        'sizes': sizes,
        'ProductSize': ProductSize.objects.all(),
        "categories": ProductCategory.objects.all(),
        "photo_products": ProductImage.objects.all(),
    })



@login_required
@require_http_methods(["POST"])  
def basket_add(request, product_id):
    try:
        data = json.loads(request.body)
        size = data.get('size', '') 
    except (ValueError, KeyError):
        return JsonResponse({'error': 'Invalid JSON or missing field'}, status=400)
    
    try:
        product = Products.objects.get(id=product_id)
        
        basket_item, created = Basket.objects.get_or_create(
            user=request.user, 
            product=product, 
            size=size, 
            defaults={'quantity': 1}  
        )
        if not created:
            basket_item.quantity += 1
            basket_item.save()

        return JsonResponse({'status': 'success', 'message': 'Product added to basket', 'basket_item_id': basket_item.id})
    except Products.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)



@login_required
def basket_remove(request , basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])