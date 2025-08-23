from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from myApp.models import Expense, Category
from django.contrib.auth import get_user_model
from decimal import Decimal


User = get_user_model()


class CategoryTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@email.com', password='test12345'
        )
        self.client.force_login(self.user)

    def test_create_category(self):
        url = reverse('myApp_api:categories_api')
        payload = {"name": "new category", "budget": 1000}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().budget, 1000)

    def test_user_can_see_his_category(self):
        Category.objects.create(name='new category',
                                        budget=1000, author=self.user)
        url = reverse('myApp_api:categories_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'new category')
        self.assertEqual(Decimal(response.data['results'][0]['budget']), 1000.00)

    def test_prevent_duplicate_category(self):
        Category.objects.create(name='new category',
                                        budget=1000, author=self.user)
        url = reverse('myApp_api:categories_api')
        payload = {"name": "new category", "budget": 1000}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 1)
        self.assertIn('You already have', response.data['non_field_errors'][0])

