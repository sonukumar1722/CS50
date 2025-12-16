from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from tracker.models import Budget, Category, RecurringTransaction, Transaction


class Command(BaseCommand):
    help = "Load deterministic demo data for the finance tracker"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            default="demo",
            help="Username for the demo account",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="password123",
            help="Password for the demo account (reset if user exists)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove the user's existing tracker data before seeding",
        )

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": f"{username}@example.com"},
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created user {username}"))
        if password:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.WARNING(f"Password set to '{password}'"))

        if options["clear"]:
            self._clear_existing(user)

        categories = self._create_categories(user)
        trans_count = self._create_transactions(user, categories, options["clear"])
        budget_count = self._create_budgets(user, categories, options["clear"])
        recurring_count = self._create_recurring(user, categories, options["clear"])

        self.stdout.write("\nSample data ready.")
        self.stdout.write(self.style.SUCCESS(f"  Transactions: {trans_count}"))
        self.stdout.write(self.style.SUCCESS(f"  Budgets: {budget_count}"))
        self.stdout.write(self.style.SUCCESS(f"  Recurring: {recurring_count}"))
        self.stdout.write(
            self.style.WARNING(f"Login with: {username} / {password}")
        )

    def _clear_existing(self, user):
        Transaction.objects.filter(user=user).delete()
        Budget.objects.filter(user=user).delete()
        RecurringTransaction.objects.filter(user=user).delete()
        Category.objects.filter(user=user).delete()
        self.stdout.write(self.style.WARNING("Cleared existing data for user."))

    def _create_categories(self, user):
        defaults = [
            {"name": "Salary", "category_type": "income", "icon": "bi-cash", "color": "#28a745"},
            {"name": "Freelance", "category_type": "income", "icon": "bi-briefcase", "color": "#20c997"},
            {"name": "Investments", "category_type": "income", "icon": "bi-graph-up", "color": "#17a2b8"},
            {"name": "Food & Dining", "category_type": "expense", "icon": "bi-cup-hot", "color": "#fd7e14"},
            {"name": "Transportation", "category_type": "expense", "icon": "bi-car-front", "color": "#6f42c1"},
            {"name": "Utilities", "category_type": "expense", "icon": "bi-lightning", "color": "#ffc107"},
            {"name": "Entertainment", "category_type": "expense", "icon": "bi-film", "color": "#e83e8c"},
            {"name": "Shopping", "category_type": "expense", "icon": "bi-bag", "color": "#dc3545"},
            {"name": "Healthcare", "category_type": "expense", "icon": "bi-heart-pulse", "color": "#007bff"},
            {"name": "Housing", "category_type": "expense", "icon": "bi-house", "color": "#6c757d"},
        ]

        categories = {}
        for payload in defaults:
            category, created = Category.objects.get_or_create(
                user=user,
                name=payload["name"],
                defaults={
                    "category_type": payload["category_type"],
                    "icon": payload["icon"],
                    "color": payload["color"],
                },
            )
            categories[payload["name"]] = category
            if created:
                self.stdout.write(f"  Added category: {payload['name']}")
        return categories

    def _create_transactions(self, user, categories, cleared):
        today = timezone.now().date()
        month_starts = [today.replace(day=1) - relativedelta(months=offset) for offset in range(0, 3)]

        transactions = []
        for month_start in month_starts:
            salary_date = self._safe_day(month_start, 25)
            transactions.append(
                {
                    "category": categories.get("Salary"),
                    "transaction_type": "income",
                    "amount": Decimal("3200.00"),
                    "description": "Monthly salary",
                    "date": salary_date,
                    "notes": "Deposit from employer",
                }
            )

            freelance_date = self._safe_day(month_start, 10)
            transactions.append(
                {
                    "category": categories.get("Freelance"),
                    "transaction_type": "income",
                    "amount": Decimal("650.00"),
                    "description": "Freelance project",
                    "date": freelance_date,
                    "notes": "Two-week contract",
                }
            )

            investments_date = self._safe_day(month_start, 5)
            transactions.append(
                {
                    "category": categories.get("Investments"),
                    "transaction_type": "income",
                    "amount": Decimal("120.00"),
                    "description": "Dividend payout",
                    "date": investments_date,
                    "notes": "ETF distribution",
                }
            )

            expense_templates = [
                (3, "Food & Dining", Decimal("32.75"), "Groceries"),
                (7, "Transportation", Decimal("42.00"), "Gas refill"),
                (11, "Entertainment", Decimal("58.00"), "Concert tickets"),
                (15, "Shopping", Decimal("140.00"), "Clothing"),
                (18, "Food & Dining", Decimal("18.50"), "Lunch out"),
                (20, "Utilities", Decimal("115.00"), "Electric bill"),
                (22, "Healthcare", Decimal("65.00"), "Pharmacy"),
                (24, "Transportation", Decimal("28.00"), "Transit card"),
                (27, "Food & Dining", Decimal("46.20"), "Weekend groceries"),
            ]

            for day, name, amount, description in expense_templates:
                transactions.append(
                    {
                        "category": categories.get(name),
                        "transaction_type": "expense",
                        "amount": amount,
                        "description": description,
                        "date": self._safe_day(month_start, day),
                        "notes": "Sample expense",
                    }
                )

        if Transaction.objects.filter(user=user).exists() and not cleared:
            self.stdout.write(
                "Existing transactions found; appending demo entries. Use --clear to reset."
            )

        created = 0
        for payload in transactions:
            Transaction.objects.create(user=user, **payload)
            created += 1

        return created

    def _create_budgets(self, user, categories, cleared):
        budgets = {
            "Food & Dining": Decimal("500.00"),
            "Transportation": Decimal("250.00"),
            "Entertainment": Decimal("180.00"),
            "Shopping": Decimal("350.00"),
            "Utilities": Decimal("220.00"),
        }

        created = 0
        for name, amount in budgets.items():
            category = categories.get(name)
            if not category:
                continue
            budget, made = Budget.objects.get_or_create(
                user=user,
                category=category,
                defaults={
                    "amount": amount,
                    "period": "monthly",
                    "is_active": True,
                    "start_date": timezone.now().date().replace(day=1),
                },
            )
            if made or cleared:
                # Refresh amount if we just cleared data, to keep values consistent
                budget.amount = amount
                budget.period = "monthly"
                budget.is_active = True
                budget.save()
            created += 1 if made else 0
        return created or Budget.objects.filter(user=user).count()

    def _create_recurring(self, user, categories, cleared):
        today = timezone.now().date()

        recurring_payloads = [
            {
                "description": "Monthly Rent",
                "category": categories.get("Housing"),
                "transaction_type": "expense",
                "amount": Decimal("1200.00"),
                "frequency": "monthly",
                "next_date": self._safe_day(today.replace(day=1), 1),
            },
            {
                "description": "Gym Membership",
                "category": categories.get("Healthcare"),
                "transaction_type": "expense",
                "amount": Decimal("50.00"),
                "frequency": "monthly",
                "next_date": self._safe_day(today.replace(day=1), 15),
            },
            {
                "description": "Music Streaming",
                "category": categories.get("Entertainment"),
                "transaction_type": "expense",
                "amount": Decimal("12.00"),
                "frequency": "monthly",
                "next_date": self._safe_day(today.replace(day=1), 10),
            },
        ]

        created = 0
        for payload in recurring_payloads:
            obj, made = RecurringTransaction.objects.update_or_create(
                user=user,
                description=payload["description"],
                defaults={
                    "category": payload["category"],
                    "transaction_type": payload["transaction_type"],
                    "amount": payload["amount"],
                    "frequency": payload["frequency"],
                    "next_date": payload["next_date"],
                    "is_active": True,
                },
            )
            created += 1 if made else 0
            if cleared and not made:
                # Keep next_date in sync after clear
                obj.next_date = payload["next_date"]
                obj.save()
        return created or RecurringTransaction.objects.filter(user=user).count()

    def _safe_day(self, month_start, day):
        month_end = month_start + relativedelta(months=1) - timedelta(days=1)
        return month_start.replace(day=min(day, month_end.day))
