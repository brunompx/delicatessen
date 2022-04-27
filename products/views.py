from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Product
from .forms import ProductListForm


def product_list_view(request):
    context = {}
    if request.method == 'POST':
        form = ProductListForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            active = form.cleaned_data['active']
            qs = Product.objects.filter(category=category)
            qs = qs.order_by('category')
            context['products'] = qs
    else:
        form = ProductListForm()
        qs = Product.objects.filter(active=True)
        context['products'] = qs
    context['form'] = form
    return render(request, 'product_list.html', context)

# View CBV to show a list of products, reeplaces by FBV with form.
# class ProductList(ListView):
#     model = Product
#     context_object_name = 'products'
    
class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    # template_name = 'base/task.html'

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'active', 'price', 'stock', 'category',]
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProductCreate, self).form_valid(form)

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('products')
    def get_queryset(self):
        # owner = self.request.user
        return self.model.objects
