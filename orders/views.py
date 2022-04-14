from django.shortcuts import render, redirect
from .models import Food
from .forms import FoodForm

def foods_home(request):
    foods = Food.objects.all()
    context = {
        "foods": foods,
    }
    return render(request, "foods_home.html", context)

def food_detail_view(request, id=None):
    food_obj = None
    if id is not None:
        food_obj = Food.objects.get(id=id)
    context = {
        "food": food_obj,
    }
    return render(request, "food_detail.html", context)

def food_create_view(request, id=None):
    form = FoodForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        food_obj = form.save()
        context['form'] = FoodForm()
        return redirect(food_obj.get_absolute_url())
    return render(request, "food_create.html", context=context)