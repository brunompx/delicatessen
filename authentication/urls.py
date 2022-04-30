from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CLoginView


urlpatterns = [
    path('accounts/login/', CLoginView.as_view()),
    path('login/', CLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

]