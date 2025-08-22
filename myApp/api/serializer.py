from myApp.models import Category, Expense
from rest_framework import serializers
from django.contrib.auth import get_user_model



class UserSerializer(serializers.ModelSerializer):
    """A serializer for showing user data."""
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'full_name', 'date_joined']


class CategorySerializer(serializers.ModelSerializer):
    author = UserSerializer()
    budget_breach = serializers.SerializerMethodField()
    total_expenses = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id',
                  'name',
                  'budget',
                  'author',
                  'budget_breach',
                  'total_expenses']
        read_only_fields = ['id', 'author']

    def get_budget_breach(self, obj):
        return obj.check_budget_breach()

    def get_total_expenses(self, obj):
        return obj.get_total_amount()


class CreateCategorySerializer(serializers.ModelSerializer):
    """A serializer for creating a new Category."""
    class Meta:
        model = Category
        fields = ['name', 'budget']

    def validate(self, attrs):
        user = self.context['request'].user
        categ_name = attrs['name']
        if Category.objects.filter(author=user,
                                   name__iexact=categ_name
                                   ).exists():
            raise serializers.ValidationError(
                "You already have a category with this name"
            )
        return attrs

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class ExpenseSerializer(serializers.ModelSerializer):
    """A Serializer for for showing expenses."""
    category = CategorySerializer()

    class Meta:
        model = Expense
        fields = ['id', 'name', 'date', 'amount', 'category']


class CreateExpenseSerializer(serializers.ModelSerializer):
    """
    A Category for creating a new expense which accepts category
    as a name and creates a new one if that category doesn't exist.
    """
    category = serializers.CharField()

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category']

    def create(self, validated_data):
        user = self.context['request'].user
        category_name = validated_data.pop("category")

        category = Category.objects.filter(
            name__iexact=category_name,
            author=user
        ).first()
        if not category:
            category = Category.objects.create(
                name=category_name,
                author=user
            )
        return Expense.objects.create(category=category, **validated_data)
