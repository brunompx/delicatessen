from django import forms
from .models import Order



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

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'comment', 'paid', 'delivered']

    def clean(self):
        data = self.cleaned_data
        name = data.get("name")
        if not name:
            self.add_error("title", f"\"{name}\" is required.")
        return data