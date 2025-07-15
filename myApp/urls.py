from django.urls import path
from . import views

app_name = 'myApp'

urlpatterns = [
    path('category_report/', views.CategoryReportView.as_view(), name='category_report'),
    path('monthly_report/', views.MonthlyReportView.as_view(), name='monthly_report'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('add_expense/', views.AddExpenseView.as_view(), name='add_expense'),
    path('', views.IndexView.as_view(), name='home'),
]
