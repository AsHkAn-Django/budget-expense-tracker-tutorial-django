from django.views.generic import TemplateView, FormView, CreateView, ListView
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm, ReportForm, CategoryReportForm
from django.urls import reverse_lazy


# Create your views here.
class IndexView(TemplateView):
    template_name = 'myApp/index.html'


class AddExpenseView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'myApp/add_expense.html'
    success_url = reverse_lazy('home')


class AddCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'myApp/add_category.html'
    success_url = reverse_lazy('add_expense')

    def form_valid(self, form):
        """Duplicate Checker."""
        category_name = form.cleaned_data.get('name')
        if Category.objects.filter(name__iexact=category_name).exists():
            form.add_error('name', 'This category already exists.')
            return self.form_invalid(form)
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
        print(category.check_budget_breach())
        return self.render_to_response(context)

