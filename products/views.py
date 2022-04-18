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


class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    
class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    # template_name = 'base/task.html'

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = '__all__'
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