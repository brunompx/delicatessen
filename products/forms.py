from django import forms
from .models import Category


class ProductListForm(forms.Form):
    name = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset = Category.objects.all(), required=False)
    active = forms.BooleanField(required=False)
