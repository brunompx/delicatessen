from django.forms import ModelForm, Textarea, Form, CharField, ModelChoiceField, BooleanField
from .models import Category, Product


class ProductListForm(Form):
    name = CharField(required=False)
    category = ModelChoiceField(queryset = Category.objects.all(), required=False)
    active = BooleanField(required=False)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'active', 'price', 'stock', 'category')
        widgets = {
            'description': Textarea(attrs={'rows': 2}),
        }