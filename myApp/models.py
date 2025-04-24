from django.db import models
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(unique=True, max_length=264)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def check_budget_breach(self):
        total = self.expenses.aggregate(total=Sum('amount'))['total'] or 0
        return total > self.budget if self.budget is not None else False


class Expense(models.Model):
    name = models.CharField(max_length=264)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')

    def __str__(self):
        return f"{self.name}: {self.amount}"
  