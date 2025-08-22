from . import views
from django.urls import path


app_name = 'myApp'

urlpatterns = [
    path('categories/', views.CategoryAPIView.as_view(), name='categories_api'),
]
