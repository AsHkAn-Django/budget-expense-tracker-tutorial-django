from django.views.generic import TemplateView, FormView, CreateView, ListView
from django.urls import reverse_lazy
import json
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm, ReportForm, CategoryReportForm
from .tasks import send_alert_email



class IndexView(TemplateView):
    template_name = 'myApp/index.html'


class AddExpenseView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'myApp/add_expense.html'
    success_url = reverse_lazy('myApp:home')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            form.fields['category'].queryset = Category.objects.filter(author=user)
        else:
            form.fields['category'].queryset = Category.objects.none()
        return form

    def form_valid(self, form):
        categ = Category.objects.get(name=form.cleaned_data['category'], author=self.request.user)
        if categ.check_budget_breach():
            send_alert_email.delay(categ.name, self.request.user.email)
            messages.error(self.request, f'Your category "{categ}" has overreached the limit!')
        return super().form_valid(form)


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'myApp/add_category.html'
    success_url = reverse_lazy('myApp:add_expense')

    def form_valid(self, form):
        """Duplicate Checker."""
        category_name = form.cleaned_data.get('name')
        if Category.objects.filter(author=self.request.user, name__iexact=category_name).exists():
            form.add_error('name', 'This category already exists.')
            return self.form_invalid(form)
        form.instance.author = self.request.user
        return super().form_valid(form)


class MonthlyReportView(LoginRequiredMixin, FormView):
    template_name = 'myApp/monthly_report.html'
    form_class = ReportForm

    def form_valid(self, form):
        month = form.cleaned_data['month']
        year = form.cleaned_data['year']
        expenses = Expense.objects.filter(
            category__author=self.request.user,
            date__month=month,
            date__year=year
        )

        total_expenses = sum(expense.amount for expense in expenses)

        # Add chart data by category
        category_totals = (
            expenses.values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('category__name')
        )

        labels = [item['category__name'] for item in category_totals]
        data = [float(item['total']) for item in category_totals]

        context = self.get_context_data(form=form)
        context['expenses'] = expenses
        context['total_expenses'] = total_expenses
        context['chart_labels'] = json.dumps(labels)
        context['chart_data'] = json.dumps(data)
        return self.render_to_response(context)


class CategoryReportView(LoginRequiredMixin, FormView):
    form_class = CategoryReportForm
    template_name = 'myApp/category_report.html'

    def form_valid(self, form):
        category = form.cleaned_data['category']
        expenses = Expense.objects.filter(category=category, category__author=self.request.user)
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        context = self.get_context_data()
        context['expenses'] = expenses
        context['total_expenses'] = total_expenses
        context['budget_breach'] = category.check_budget_breach()
        context['expenses_list'] = json.dumps([expense.name for expense in expenses])
        context['amounts_list'] = json.dumps([float(expense.amount) for expense in expenses])

        return self.render_to_response(context)

