from django.urls import path
from .views import (IndexView, AddExpenseView, AddCategoryView,
                    MonthlyReportView, CategoryReportView)

urlpatterns = [
    path('category_report/', CategoryReportView.as_view(), name='category_report'),
    path('monthly_report/', MonthlyReportView.as_view(), name='monthly_report'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('add_expense/', AddExpenseView.as_view(), name='add_expense'),
    path('', IndexView.as_view(), name='home'),
]
