from django.urls import reverse_lazy
from users.forms import UserAuthForm, UserRegForm
from django.contrib.auth.views import LoginView
from django.views.generic import FormView, CreateView

# Create your views here.

class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = UserAuthForm
    extra_context = {'title': 'Вход'}
    
    def get_success_url(self) -> str:
        return reverse_lazy('mess:list')
    
    
class RegUser(CreateView):
    template_name = 'users/register_user.html'
    form_class = UserRegForm
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация', 'catg_selected': 6}
    