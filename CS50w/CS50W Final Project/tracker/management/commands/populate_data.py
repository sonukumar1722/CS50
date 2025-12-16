import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Category, Transaction, Budget, RecurringTransaction
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the database with random financial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='testuser',
            help='Username for the test account'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all transactions before populating'
        )

    def handle(self, *args, **options):
        username = options['username']
        
        # Get or create user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@example.com'}
        )
        
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created user: {username}')
            )
        
        # Clear existing data if requested
        if options['clear']:
            Transaction.objects.filter(user=user).delete()
            RecurringTransaction.objects.filter(user=user).delete()
            Budget.objects.filter(user=user).delete()
            self.stdout.write(
                self.style.WARNING('⊘ Cleared existing transactions and budgets')
            )
        
        # Create or get default categories
        categories = self._create_categories(user)
        
        # Generate random transactions
        self._create_transactions(user, categories)
        
        # Create budgets
        self._create_budgets(user, categories)
        
        # Create recurring transactions
        self._create_recurring(user, categories)
        
        self.stdout.write(
            self.style.SUCCESS('\n✓ Data population complete!')
        )
        self.stdout.write(
            self.style.WARNING(f'Login with: {username} / password123')
        )

    def _create_categories(self, user):
        """Create or get default categories"""
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
        
        categories = {}
        for cat_data in defaults:
            cat, created = Category.objects.get_or_create(
                user=user,
                name=cat_data['name'],
                defaults={
                    'category_type': cat_data['category_type'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color']
                }
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(
                    f'  Created category: {cat_data["name"]}'
                )
        
        return categories

    def _create_transactions(self, user, categories):
        """Generate random transactions for the last 3 months"""
        self.stdout.write('\nGenerating transactions...')
        
        today = timezone.now().date()
        start_date = today - timedelta(days=90)
        
        # Income transactions (less frequent)
        income_data = [
            ('Salary', 3500, 25),  # Monthly salary around the 25th
            ('Freelance', random.randint(200, 800), None),
            ('Investments', random.randint(50, 300), None),
        ]
        
        # Expense transactions (more frequent and varied)
        expense_data = [
            ('Food & Dining', [random.randint(10, 50) for _ in range(3)]),
            ('Transportation', [random.randint(20, 80) for _ in range(2)]),
            ('Shopping', [random.randint(30, 200) for _ in range(2)]),
            ('Entertainment', [random.randint(15, 100) for _ in range(2)]),
            ('Utilities', [random.randint(100, 200) for _ in range(1)]),
            ('Healthcare', [random.randint(50, 300) for _ in range(1)]),
        ]
        
        # Create income transactions
        current_date = start_date
        while current_date <= today:
            for name, amount, day_of_month in income_data:
                category = categories.get(name)
                if not category:
                    continue
                
                # Salary on specific day
                if name == 'Salary' and current_date.day == day_of_month:
                    Transaction.objects.create(
                        user=user,
                        category=category,
                        transaction_type='income',
                        amount=Decimal(str(amount)),
                        description=f'{name} deposit',
                        date=current_date,
                        notes='Monthly salary'
                    )
                # Random other income
                elif name != 'Salary' and random.random() < 0.05:  # 5% chance
                    Transaction.objects.create(
                        user=user,
                        category=category,
                        transaction_type='income',
                        amount=Decimal(str(amount)),
                        description=f'{name} received',
                        date=current_date
                    )
            
            # Create expense transactions
            for name, amounts in expense_data:
                category = categories.get(name)
                if not category:
                    continue
                
                # Random chance of expense each day
                if random.random() < (0.3 if name == 'Food & Dining' else 0.15):
                    amount = random.choice(amounts)
                    Transaction.objects.create(
                        user=user,
                        category=category,
                        transaction_type='expense',
                        amount=Decimal(str(amount)),
                        description=f'{name} expense',
                        date=current_date
                    )
            
            current_date += timedelta(days=1)
        
        trans_count = Transaction.objects.filter(user=user).count()
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ Created {trans_count} transactions')
        )

    def _create_budgets(self, user, categories):
        """Create monthly budgets for expense categories"""
        self.stdout.write('\nCreating budgets...')
        
        budget_limits = {
            'Food & Dining': 500,
            'Transportation': 300,
            'Entertainment': 200,
            'Shopping': 400,
            'Utilities': 200,
        }
        
        for category_name, amount in budget_limits.items():
            category = categories.get(category_name)
            if not category:
                continue
            
            Budget.objects.get_or_create(
                user=user,
                category=category,
                defaults={
                    'amount': Decimal(str(amount)),
                    'period': 'monthly',
                    'is_active': True
                }
            )
        
        budget_count = Budget.objects.filter(user=user).count()
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ Created {budget_count} budgets')
        )

    def _create_recurring(self, user, categories):
        """Create recurring transactions"""
        self.stdout.write('\nCreating recurring transactions...')
        
        today = timezone.now().date()
        
        # Monthly rent
        category = categories.get('Housing')
        if category:
            RecurringTransaction.objects.get_or_create(
                user=user,
                description='Monthly Rent',
                defaults={
                    'category': category,
                    'transaction_type': 'expense',
                    'amount': Decimal('1200'),
                    'frequency': 'monthly',
                    'next_date': today.replace(day=1),
                    'is_active': True
                }
            )
        
        # Gym membership
        category = categories.get('Healthcare')
        if category:
            RecurringTransaction.objects.get_or_create(
                user=user,
                description='Gym Membership',
                defaults={
                    'category': category,
                    'transaction_type': 'expense',
                    'amount': Decimal('50'),
                    'frequency': 'monthly',
                    'next_date': today.replace(day=15),
                    'is_active': True
                }
            )
        
        recurring_count = RecurringTransaction.objects.filter(user=user).count()
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ Created {recurring_count} recurring transactions')
        )
