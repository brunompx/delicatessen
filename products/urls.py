from django.urls import path
from .views import ProductList, ProductDetail


urlpatterns = [
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # path('register/', RegisterPage.as_view(), name='register'),

    path('product/', ProductList.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product'),
    # path('product-create/', TaskCreate.as_view(), name='task-create'),
    # path('product-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    # path('product-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    # path('product-reorder/', TaskReorder.as_view(), name='task-reorder'),
]