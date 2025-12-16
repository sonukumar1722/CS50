from django.contrib import admin
from .models import Category, Transaction, Budget, RecurringTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'user', 'color']
    list_filter = ['category_type', 'user']
    search_fields = ['name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'transaction_type', 'category', 'date', 'user']
    list_filter = ['transaction_type', 'category', 'date', 'user']
    search_fields = ['description', 'notes']
    date_hierarchy = 'date'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'period', 'is_active', 'user']
    list_filter = ['period', 'is_active', 'user']


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'frequency', 'next_date', 'is_active', 'user']
    list_filter = ['frequency', 'is_active', 'transaction_type', 'user']
    search_fields = ['description']
