from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, max_length=264)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Expense(models.Model):
    name = models.CharField(max_length=264)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
