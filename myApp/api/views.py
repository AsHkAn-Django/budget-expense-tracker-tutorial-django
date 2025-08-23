from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Sum, Count, Max, Min, Avg
from django.db.models.functions import Round
from django.utils.timezone import now

from myApp.tasks import send_alert_email
from .serializer import (ExpenseSerializer, CreateCategorySerializer,
                         CreateExpenseSerializer, CategorySerializer)
from myApp.models import Expense, Category



class CategoryAPIView(APIView):
    """
    A view to show the categories or create a new one
    for an authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Bring the list of catogories for this user."""
        categories = Category.objects.filter(author=request.user)
        serialized_categs = CategorySerializer(categories,
                                               many=True,
                                               context={'request':request})
        return Response(serialized_categs.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new Category."""
        serializer = CreateCategorySerializer(data=request.data,
                                              context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "The category has been created"},
                        status=status.HTTP_201_CREATED)


class ExpenseAPIView(APIView):
    """
    A view for showing and creating a new Expense.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Show the list of expenses."""
        expenses = Expense.objects.filter(category__author=request.user)
        serialized_exp = ExpenseSerializer(expenses, many=True,
                                           context={'request': request})
        return Response(serialized_exp.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new expense."""
        serializer = CreateExpenseSerializer(data=request.data,
                                             context={'request': request})
        serializer.is_valid(raise_exception=True)
        expense = serializer.save()
        categ = expense.category
        if categ.check_budget_breach():
            send_alert_email.delay(categ.name, request.user.email)

        return Response({"Success": "The expense has been saved."},
                        status=status.HTTP_201_CREATED)


class AnalyticsAPIView(APIView):
    """
    Give Users Analatics about their expenses.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = Expense.objects.filter(
            category__author=user
            ).values("category__name").annotate(
            total=Sum("amount"),
            number_of_expenses=Count("id"),
            highest_expense=Max("amount"),
            lowest_expense=Min("amount"),
            average_expense=Round(Avg("amount"), 2)
            ).order_by("-total")

        today_date = now().date()

        today_expenses = Expense.objects.filter(
            date__date=today_date, category__author=user).aggregate(
                total_spent_today=Sum("amount"),
                number_of_expenses_today=Count("id"),
                highest_expense_today=Max('amount'),
                lowest_expense_today=Min('amount'),
                average_expenses_today=Round(Avg('amount'), 2)
            )

        total_expenses = Expense.objects.filter(
            category__author=user).aggregate(
                total_spent=Sum("amount")or 0,
                total_number_of_expenses=Count("id"),
                total_highest_expense=Max('amount'),
                total_lowest_expense=Min('amount'),
                total_average_expenses=Round(Avg('amount'), 2)
            )

        return Response(
            {
                "by_category": data,
                "today": today_expenses,
                "total": total_expenses,
            },
            status=status.HTTP_200_OK)

