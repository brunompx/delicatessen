from django import forms
from .models import Order, Category, Food, OrderItem



class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'description', 'recipe', 'status', 'price', 'category']
    
    def clean(self):
        data = self.cleaned_data #dic
        name = data.get('name')
        qs = Food.objects.filter(name=name)
        if qs.exists():
            self.add_error('title', f"\"{name}\" already exists.")
        return data