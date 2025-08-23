from django.contrib import admin
from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'budget', 'author']
    filter = ['name', 'budget', 'author']
    search_fields = ['name', 'budget', 'author']
    raw_id_fields = ['author']



@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'amount', 'category']
    filter = ['name', 'date', 'amount', 'category']
    search_fields = ['name', 'date', 'amount', 'category']

