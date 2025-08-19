from django.contrib.auth import get_user_model
from .forms import CustomUserCreationFrom
from django.views import generic
from django.urls import reverse_lazy



class UserCreateView(generic.CreateView):
    model = get_user_model()
    template_name = "users/signup.html"
    form_class = CustomUserCreationFrom
    success_url = reverse_lazy('users:login')
