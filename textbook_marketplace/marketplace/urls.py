# backend/textbook_marketplace/marketplace/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProtectedView, SignupView, CustomTokenObtainPairView, TextbookViewSet, UserViewSet, OrderViewSet, UserDetailView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('textbooks/', views.TextbookListView.as_view(), name='textbook-list'),
    path('textbook/<int:pk>/', views.TextbookDetailView.as_view(), name='textbook-detail'),
    path('textbook/<int:pk>/image/', views.TextbookImageView.as_view()),
    path('textbook/create/', TextbookViewSet.as_view({'post': 'create'}), name='textbook_create'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('users/me/', UserDetailView.as_view(), name='user-detail'),
]
