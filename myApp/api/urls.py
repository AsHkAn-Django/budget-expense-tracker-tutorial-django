from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'myApp'

urlpatterns = [
    path('categories/', views.CategoryAPIView.as_view(), name='categories_api'),
    path('expenses/', views.ExpenseAPIView.as_view(), name='expenses_api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('analytics/', views.AnalyticsAPIView.as_view(), name='analytics_api'),
]
