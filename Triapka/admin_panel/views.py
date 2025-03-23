from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView
from products.models import Products , Brands ,ProductCategory , Size , ProductSize


from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from decimal import Decimal

from django.views.generic import UpdateView
from .forms import ProductForm 
from django.urls import reverse_lazy
from django.core.paginator import Paginator

# Create your views here.
class AdminProducts(TemplateView):
    template_name = 'admin_panel/admin_products.html'
    
    def get_context_data(self, **kwargs):
        context = super(AdminProducts, self).get_context_data(**kwargs)
        all_products = Products.objects.all().order_by('-id')  
        paginator = Paginator(all_products, 15)  
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['products'] = all_products  
        context['paginator'] = paginator
        context['page_number'] = page_number
        context['page_obj'] = page_obj
        return context
    
class FormAddProducts(TemplateView):
    template_name = 'admin_panel/form_add_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unique_genders'] = Products.GenderChoices.choices
        context['all_brands'] = Brands.objects.all()
        context['all_categories'] = ProductCategory.objects.all()
        context['all_size'] = Size.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # Получаем данные из формы
        name = request.POST['name']
        description = request.POST['description']
        price = Decimal(request.POST['price'])
        gender = request.POST['gender']
        category_id = request.POST['category']
        brand_id = request.POST['brands']
        image = request.FILES.get('image')  # Может быть None, если изображение не загружено

        # Создаем новый продукт
        category = ProductCategory.objects.get(id=category_id)
        brand = Brands.objects.get(id=brand_id)
        new_product = Products(
            name=name,
            description=description,
            price=price,
            gender=gender,
            category=category,
            brands=brand,
            image=image
        )
        new_product.save()  # Сохраняем продукт в базе данных

        # Обрабатываем размеры и количество
        sizes = request.POST.getlist('sizes[]')
        quantities = request.POST.getlist('quantities[]')
        for size, quantity in zip(sizes, quantities):
            if quantity:  # Проверяем, есть ли количество
                size_instance = Size.objects.get(size=size)
                ProductSize.objects.create(
                    product=new_product,
                    size=size_instance,
                    quantity=int(quantity)
                )

        return HttpResponseRedirect(reverse('admin_panel:admin_products'))
    

class FormEditProducts(UpdateView):
    model = Products
    form_class = ProductForm
    template_name = 'admin_panel/form_edit_products.html'
    success_url = reverse_lazy('admin_panel:admin_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передайте все доступные размеры в контекст, чтобы использовать их в шаблоне
        context['all_sizes'] = Size.objects.all()
        return context

    def form_valid(self, form):
        # Сохранение основного объекта продукта
        self.object = form.save()
        
        # Получение данных о размерах и количестве из формы
        sizes_ids = self.request.POST.getlist('sizes[]')
        quantities = self.request.POST.getlist('quantities[]')

        # Обновление информации о размерах и количестве
        # Сначала удаляем все существующие связи размеров с продуктом
        ProductSize.objects.filter(product=self.object).exclude(size__id__in=sizes_ids).delete()

        # Затем обновляем существующие и создаем новые связи
        for size_id, quantity in zip(sizes_ids, quantities):
            size_instance = get_object_or_404(Size, id=size_id)
            product_size, created = ProductSize.objects.update_or_create(
                product=self.object, 
                size=size_instance, 
                defaults={'quantity': int(quantity)}
            )

        # Перенаправление на страницу успеха
        return HttpResponseRedirect(self.get_success_url())

class AdminOrders(TemplateView):
    template_name = 'admin_panel/admin_orders.html'

    def get_context_data(self, **kwargs):
        context = super(AdminOrders, self).get_context_data(**kwargs)
        all_orders = Order.objects.all().order_by('-id')  # Получаем все заказы, отсортированные по убыванию идентификатора
        paginator = Paginator(all_orders, 10)  # Создаем пагинатор для заказов, 6 на страницу
        page_number = self.request.GET.get('page')  # Получаем номер текущей страницы из запроса
        page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

        # Обновляем контекст
        context['orders'] = all_orders  # Может быть необязательно, если вы используете page_obj для отображения заказов
        context['paginator'] = paginator
        context['page_number'] = page_number
        context['page_obj'] = page_obj
        
        return context
    



class AdminBrands(TemplateView):
    template_name = 'admin_panel/admin_brands.html'
    
    def get_context_data(self, **kwargs):
        context = super(AdminBrands, self).get_context_data(**kwargs)
        all_brands = Brands.objects.all().order_by('-id')  
        paginator = Paginator(all_brands, 15)  
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['brands'] = all_brands 
        context['paginator'] = paginator
        context['page_number'] = page_number
        context['page_obj'] = page_obj
        return context
    

class FormAddBrands(TemplateView):
    template_name = 'admin_panel/form_add_brands.html'
    
    def post(self, request, *args, **kwargs):
        # Получаем данные из формы
        name = request.POST['name']

        # Создаем новый продукт
        new_product = Products(
            name=name,
        )
        new_product.save()  


        return HttpResponseRedirect(reverse('admin_panel:admin_brands'))