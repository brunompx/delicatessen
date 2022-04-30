
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class CLoginView(LoginView):
    print('llega')
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('orders')

