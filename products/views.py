from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect

from .models import Product
from .forms import ProductListForm, ProductForm

@login_required
def product_list_view(request):
    context = {}
    if request.method == 'POST':
        form = ProductListForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            active = form.cleaned_data['active']
            print(name)
            print(category)
            print(active)
            q_filter = Q()
            q_filter.add(Q(user=request.user), Q.AND)
            if name:
                q_filter.add(Q(name__icontains=name), Q.AND)
            if category:
                q_filter.add(Q(category=category), Q.AND)
            if not active:
                q_filter.add(Q(active=True), Q.AND)
            qs = Product.objects.filter(q_filter)
            qs = qs.order_by('category')
            context['products'] = qs

    else:
        form = ProductListForm()
        qs = Product.objects.filter(user=request.user, active=True)
        context['products'] = qs
    context['form'] = form
    return render(request, 'product_list.html', context)

# View CBV to show a list of products, reeplaced by FBV product_list_view.
# class ProductList(ListView):
#     model = Product
#     context_object_name = 'products'
    
class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
    # template_name = 'base/task.html'

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    # fields = ['name', 'description', 'active', 'price', 'stock', 'category',]
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProductCreate, self).form_valid(form)

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    # fields = '__all__'
    success_url = reverse_lazy('products')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('products')
    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(user=user)
