from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('transactions/', views.transactions, name='transactions'),
    path('api/transactions/', views.api_transactions, name='api_transactions'),
    path('api/transactions/<int:pk>/', views.api_transaction_detail, name='api_transaction_detail'),
    
    path('categories/', views.categories, name='categories'),
    path('api/categories/', views.api_categories, name='api_categories'),
    path('api/categories/<int:pk>/', views.api_category_detail, name='api_category_detail'),
    
    path('budgets/', views.budgets, name='budgets'),
    path('api/budgets/', views.api_budgets, name='api_budgets'),
    path('api/budgets/<int:pk>/', views.api_budget_detail, name='api_budget_detail'),
    
    path('recurring/', views.recurring, name='recurring'),
    path('api/recurring/', views.api_recurring, name='api_recurring'),
    path('api/recurring/<int:pk>/', views.api_recurring_detail, name='api_recurring_detail'),
    
    path('api/dashboard-data/', views.api_dashboard_data, name='api_dashboard_data'),
    path('export/csv/', views.export_csv, name='export_csv'),
]
