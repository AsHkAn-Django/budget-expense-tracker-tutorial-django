from .serializer import (ExpenseSerializer, CreateCategorySerializer,
                         CreateExpenseSerializer, CategorySerializer)
from rest_framework.views import APIView
from myApp.models import Expense, Category
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status



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
        serializer.save()
        return Response({"Success": "The expense has been saved."},
                        status=status.HTTP_201_CREATED)
