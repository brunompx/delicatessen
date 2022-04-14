from django.contrib import admin
from django.urls import path, include
from orders.views import (
    foods_home,
    food_detail_view,
    food_create_view
)

urlpatterns = [
    # path('', orders_home, name='orders_home'),
    path('foods/', foods_home, name='foods_home'),
    path('foods/create/', food_create_view, name='food_create'),
    path('foods/<int:id>/', food_detail_view, name='food_detail'),
]