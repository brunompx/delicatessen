from django import forms
# from .models import Order, Category, Product, OrderItem



# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'description', 'status', 'price', 'category']
    
#     def clean(self):
#         data = self.cleaned_data #dic
#         name = data.get('name')
#         qs = Product.objects.filter(name=name)
#         if qs.exists():
#             self.add_error('title', f"\"{name}\" already exists.")
#         return data