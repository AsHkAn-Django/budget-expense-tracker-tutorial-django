from django.views.generic import TemplateView, FormView, CreateView, ListView
from django.urls import reverse_lazy
import json
from django.contrib import messages

from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm, ReportForm, CategoryReportForm
from .tasks import send_alert_email


# Create your views here.
class IndexView(TemplateView):
    template_name = 'myApp/index.html'


class AddExpenseView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'myApp/add_expense.html'
    success_url = reverse_lazy('home')
    
    def get_form(self):
        form = super().get_form()
        form.fields['category'].queryset = Category.objects.filter(author=self.request.user)
        return form
    
    def form_valid(self, form):
        categ = Category.objects.get(name=form.cleaned_data['category'], author=self.request.user   )
        if categ.check_budget_breach():
            send_alert_email.delay(categ.name, self.request.user.email)
            messages.error(self.request, f'Your category "{categ}" has overreached the limit!')
        return super().form_valid(form)


class AddCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'myApp/add_category.html'
    success_url = reverse_lazy('add_expense')

    def form_valid(self, form):
        """Duplicate Checker."""
        category_name = form.cleaned_data.get('name')
        if Category.objects.filter(author=self.request.user, name__iexact=category_name).exists():
            form.add_error('name', 'This category already exists.')
            return self.form_invalid(form)
        form.instance.author = self.request.user
        return super().form_valid(form)


class MonthlyReportView(FormView):
    template_name = 'myApp/monthly_report.html'
    form_class = ReportForm

    def form_valid(self, form):
        month = form.cleaned_data['month']
        year = form.cleaned_data['year']
        expenses = Expense.objects.filter(date__month=month, date__year=year)

        total_expenses = sum(expense.amount for expense in expenses)

        context = self.get_context_data(form=form)

        context['expenses'] = expenses
        context['total_expenses'] = total_expenses
        return self.render_to_response(context)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['expenses'] = Expense.objects.none()
        context['total_expenses'] = 0
        return self.render_to_response(context)


class CategoryReportView(FormView):
    form_class = CategoryReportForm
    template_name = 'myApp/category_report.html'

    def form_valid(self, form):
        category = form.cleaned_data['category']
        expenses = Expense.objects.filter(category=category)
        total_expenses = sum(expense.amount for expense in expenses)
        context = self.get_context_data()
        context['expenses'] = expenses
        context['total_expenses'] = total_expenses
        context['budget_breach'] = category.check_budget_breach()
        context['expenses_list'] = json.dumps([expense.name for expense in expenses])
        context['amounts_list'] = json.dumps([float(expense.amount) for expense in expenses])

        return self.render_to_response(context)

