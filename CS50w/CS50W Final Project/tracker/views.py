import csv
import json
from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Q
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .models import Category, Transaction, Budget, RecurringTransaction


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            create_default_categories(user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})


def create_default_categories(user):
    defaults = [
        {'name': 'Salary', 'category_type': 'income', 'icon': 'bi-cash', 'color': '#28a745'},
        {'name': 'Freelance', 'category_type': 'income', 'icon': 'bi-briefcase', 'color': '#20c997'},
        {'name': 'Investments', 'category_type': 'income', 'icon': 'bi-graph-up', 'color': '#17a2b8'},
        {'name': 'Food & Dining', 'category_type': 'expense', 'icon': 'bi-cup-hot', 'color': '#fd7e14'},
        {'name': 'Transportation', 'category_type': 'expense', 'icon': 'bi-car-front', 'color': '#6f42c1'},
        {'name': 'Utilities', 'category_type': 'expense', 'icon': 'bi-lightning', 'color': '#ffc107'},
        {'name': 'Entertainment', 'category_type': 'expense', 'icon': 'bi-film', 'color': '#e83e8c'},
        {'name': 'Shopping', 'category_type': 'expense', 'icon': 'bi-bag', 'color': '#dc3545'},
        {'name': 'Healthcare', 'category_type': 'expense', 'icon': 'bi-heart-pulse', 'color': '#007bff'},
        {'name': 'Housing', 'category_type': 'expense', 'icon': 'bi-house', 'color': '#6c757d'},
    ]
    for cat in defaults:
        Category.objects.create(user=user, **cat)


@login_required
def dashboard(request):
    process_recurring_transactions(request.user)
    return render(request, 'tracker/dashboard.html')


@login_required
def transactions(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'tracker/transactions.html', {'categories': categories})


@login_required
def categories(request):
    return render(request, 'tracker/categories.html')


@login_required
def budgets(request):
    categories = Category.objects.filter(user=request.user, category_type='expense')
    return render(request, 'tracker/budgets.html', {'categories': categories})


@login_required
def recurring(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'tracker/recurring.html', {'categories': categories})


def process_recurring_transactions(user):
    today = timezone.now().date()
    recurring = RecurringTransaction.objects.filter(user=user, is_active=True, next_date__lte=today)
    
    for rec in recurring:
        Transaction.objects.create(
            user=user,
            category=rec.category,
            transaction_type=rec.transaction_type,
            amount=rec.amount,
            description=rec.description,
            date=rec.next_date,
            notes=f"Auto-generated from recurring: {rec.description}"
        )
        
        if rec.frequency == 'daily':
            rec.next_date += timedelta(days=1)
        elif rec.frequency == 'weekly':
            rec.next_date += timedelta(weeks=1)
        elif rec.frequency == 'biweekly':
            rec.next_date += timedelta(weeks=2)
        elif rec.frequency == 'monthly':
            rec.next_date += relativedelta(months=1)
        elif rec.frequency == 'yearly':
            rec.next_date += relativedelta(years=1)
        rec.save()


@login_required
@require_http_methods(["GET", "POST"])
def api_transactions(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(user=request.user)
        
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        category_id = request.GET.get('category')
        trans_type = request.GET.get('type')
        search = request.GET.get('search')
        
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
        if category_id:
            transactions = transactions.filter(category_id=category_id)
        if trans_type:
            transactions = transactions.filter(transaction_type=trans_type)
        if search:
            transactions = transactions.filter(
                Q(description__icontains=search) | Q(notes__icontains=search)
            )
        
        data = [{
            'id': t.id,
            'category': {'id': t.category.id, 'name': t.category.name, 'color': t.category.color} if t.category else None,
            'transaction_type': t.transaction_type,
            'amount': str(t.amount),
            'description': t.description,
            'date': t.date.isoformat(),
            'notes': t.notes or ''
        } for t in transactions]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        category = None
        if data.get('category_id'):
            category = get_object_or_404(Category, id=data['category_id'], user=request.user)
        
        transaction = Transaction.objects.create(
            user=request.user,
            category=category,
            transaction_type=data['transaction_type'],
            amount=Decimal(data['amount']),
            description=data['description'],
            date=data.get('date', timezone.now().date()),
            notes=data.get('notes', '')
        )
        return JsonResponse({'id': transaction.id, 'success': True})


@login_required
@require_http_methods(["PUT", "DELETE"])
def api_transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        category = None
        if data.get('category_id'):
            category = get_object_or_404(Category, id=data['category_id'], user=request.user)
        
        transaction.category = category
        transaction.transaction_type = data['transaction_type']
        transaction.amount = Decimal(data['amount'])
        transaction.description = data['description']
        transaction.date = data.get('date', transaction.date)
        transaction.notes = data.get('notes', '')
        transaction.save()
        return JsonResponse({'success': True})
    
    elif request.method == 'DELETE':
        transaction.delete()
        return JsonResponse({'success': True})


@login_required
@require_http_methods(["GET", "POST"])
def api_categories(request):
    if request.method == 'GET':
        categories = Category.objects.filter(user=request.user)
        data = [{
            'id': c.id,
            'name': c.name,
            'category_type': c.category_type,
            'icon': c.icon,
            'color': c.color
        } for c in categories]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        category = Category.objects.create(
            user=request.user,
            name=data['name'],
            category_type=data['category_type'],
            icon=data.get('icon', 'bi-tag'),
            color=data.get('color', '#6c757d')
        )
        return JsonResponse({'id': category.id, 'success': True})


@login_required
@require_http_methods(["PUT", "DELETE"])
def api_category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        category.name = data['name']
        category.category_type = data['category_type']
        category.icon = data.get('icon', category.icon)
        category.color = data.get('color', category.color)
        category.save()
        return JsonResponse({'success': True})
    
    elif request.method == 'DELETE':
        category.delete()
        return JsonResponse({'success': True})


@login_required
@require_http_methods(["GET", "POST"])
def api_budgets(request):
    if request.method == 'GET':
        budgets = Budget.objects.filter(user=request.user, is_active=True)
        today = timezone.now().date()
        
        data = []
        for b in budgets:
            if b.period == 'weekly':
                start = today - timedelta(days=today.weekday())
                end = start + timedelta(days=6)
            elif b.period == 'monthly':
                start = today.replace(day=1)
                end = (start + relativedelta(months=1)) - timedelta(days=1)
            else:
                start = today.replace(month=1, day=1)
                end = today.replace(month=12, day=31)
            
            spent = Transaction.objects.filter(
                user=request.user,
                category=b.category,
                transaction_type='expense',
                date__gte=start,
                date__lte=end
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
            
            data.append({
                'id': b.id,
                'category': {'id': b.category.id, 'name': b.category.name, 'color': b.category.color},
                'amount': str(b.amount),
                'spent': str(spent),
                'period': b.period,
                'percentage': min(100, int((spent / b.amount) * 100)) if b.amount > 0 else 0
            })
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        category = get_object_or_404(Category, id=data['category_id'], user=request.user)
        budget = Budget.objects.create(
            user=request.user,
            category=category,
            amount=Decimal(data['amount']),
            period=data['period']
        )
        return JsonResponse({'id': budget.id, 'success': True})


@login_required
@require_http_methods(["PUT", "DELETE"])
def api_budget_detail(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        category = get_object_or_404(Category, id=data['category_id'], user=request.user)
        budget.category = category
        budget.amount = Decimal(data['amount'])
        budget.period = data['period']
        budget.save()
        return JsonResponse({'success': True})
    
    elif request.method == 'DELETE':
        budget.delete()
        return JsonResponse({'success': True})


@login_required
@require_http_methods(["GET", "POST"])
def api_recurring(request):
    if request.method == 'GET':
        recurring = RecurringTransaction.objects.filter(user=request.user)
        data = [{
            'id': r.id,
            'category': {'id': r.category.id, 'name': r.category.name, 'color': r.category.color} if r.category else None,
            'transaction_type': r.transaction_type,
            'amount': str(r.amount),
            'description': r.description,
            'frequency': r.frequency,
            'next_date': r.next_date.isoformat(),
            'is_active': r.is_active
        } for r in recurring]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        category = None
        if data.get('category_id'):
            category = get_object_or_404(Category, id=data['category_id'], user=request.user)
        
        recurring = RecurringTransaction.objects.create(
            user=request.user,
            category=category,
            transaction_type=data['transaction_type'],
            amount=Decimal(data['amount']),
            description=data['description'],
            frequency=data['frequency'],
            next_date=data['next_date'],
            is_active=data.get('is_active', True)
        )
        return JsonResponse({'id': recurring.id, 'success': True})


@login_required
@require_http_methods(["PUT", "DELETE"])
def api_recurring_detail(request, pk):
    recurring = get_object_or_404(RecurringTransaction, pk=pk, user=request.user)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        category = None
        if data.get('category_id'):
            category = get_object_or_404(Category, id=data['category_id'], user=request.user)
        
        recurring.category = category
        recurring.transaction_type = data['transaction_type']
        recurring.amount = Decimal(data['amount'])
        recurring.description = data['description']
        recurring.frequency = data['frequency']
        recurring.next_date = data['next_date']
        recurring.is_active = data.get('is_active', True)
        recurring.save()
        return JsonResponse({'success': True})
    
    elif request.method == 'DELETE':
        recurring.delete()
        return JsonResponse({'success': True})


@login_required
def api_dashboard_data(request):
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + relativedelta(months=1)) - timedelta(days=1)
    
    period = request.GET.get('period', 'month')
    if period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
    else:
        start_date = start_of_month
        end_date = end_of_month
    
    transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    total_income = transactions.filter(transaction_type='income').aggregate(
        total=Sum('amount'))['total'] or Decimal('0')
    total_expenses = transactions.filter(transaction_type='expense').aggregate(
        total=Sum('amount'))['total'] or Decimal('0')
    
    expense_by_category = transactions.filter(
        transaction_type='expense',
        category__isnull=False
    ).values('category__name', 'category__color').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    daily_data = {}
    current = start_date
    while current <= end_date:
        daily_data[current.isoformat()] = {'income': Decimal('0'), 'expense': Decimal('0')}
        current += timedelta(days=1)
    
    for t in transactions:
        date_key = t.date.isoformat()
        if date_key in daily_data:
            daily_data[date_key][t.transaction_type] += t.amount
    
    recent_transactions = [{
        'id': t.id,
        'description': t.description,
        'amount': str(t.amount),
        'transaction_type': t.transaction_type,
        'date': t.date.isoformat(),
        'category': t.category.name if t.category else 'Uncategorized'
    } for t in transactions[:10]]
    
    return JsonResponse({
        'total_income': str(total_income),
        'total_expenses': str(total_expenses),
        'balance': str(total_income - total_expenses),
        'expense_by_category': [{
            'name': e['category__name'],
            'color': e['category__color'],
            'total': str(e['total'])
        } for e in expense_by_category],
        'daily_data': {k: {'income': str(v['income']), 'expense': str(v['expense'])} 
                       for k, v in daily_data.items()},
        'recent_transactions': recent_transactions,
        'period': period,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    })


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Type', 'Category', 'Description', 'Amount', 'Notes'])
    
    transactions = Transaction.objects.filter(user=request.user)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)
    
    for t in transactions:
        writer.writerow([
            t.date.isoformat(),
            t.transaction_type,
            t.category.name if t.category else 'Uncategorized',
            t.description,
            str(t.amount),
            t.notes or ''
        ])
    
    return response
