from django import forms
from products.models import Products, ProductCategory, Brands 

class ProductForm(forms.ModelForm):
    # Используем более стандартные и понятные имена классов
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Product Name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea-field', 'placeholder': 'Product Description'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Price'}))
    # Предполагаем, что у вас уже есть загрузка изображений
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), required=False)
    gender = forms.ChoiceField(choices=Products.GenderChoices.choices, widget=forms.Select(attrs={'class': 'select-field'}))
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), widget=forms.Select(attrs={'class': 'select-field'}))
    brands = forms.ModelChoiceField(queryset=Brands.objects.all(), widget=forms.Select(attrs={'class': 'select-field'}))
    

    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'image', 'gender', 'category', 'brands']
