from django import forms
from .models import Category, Expense
import datetime


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'name', 'amount']



class ReportForm(forms.Form):
    MONTH_CHOICES = [(i, datetime.date(1900, i, 1).strftime('%B')) for i in range(1, 13)]  
    YEAR_CHOICES = [(y, y) for y in range(2000, datetime.datetime.now().year + 1)]

    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Month"
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Year"
    )



class CategoryReportForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category']

