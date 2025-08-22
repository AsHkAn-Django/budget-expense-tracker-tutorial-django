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

