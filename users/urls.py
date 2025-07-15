from . import views
from django.urls import path, include


app_name = 'users'

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('signup/', views.UserCreateView.as_view(), name='signup'),
]