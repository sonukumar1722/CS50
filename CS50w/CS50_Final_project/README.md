# Personal Finance Tracker

A comprehensive web application for managing personal finances, tracking expenses, setting budgets, and visualizing spending patterns. Built with Django and JavaScript for the CS50W Capstone Project.

## Distinctiveness and Complexity

This project is distinct from other CS50W projects in several key ways:

1. **Not a Social Network**: Unlike Project 4, this application focuses on personal financial management rather than user interactions, posts, likes, or follows. There is no social component - each user's data is completely private.

2. **Not an E-commerce Site**: Unlike Project 2, this is not about buying or selling products. There are no shopping carts, product listings, or payment processing. Instead, it's a personal tool for tracking where money goes after it's already been spent.

3. **Unique Domain**: Personal finance tracking involves unique concepts like:
   - Budget monitoring with spending limits and progress tracking
   - Recurring transaction automation for bills and subscriptions
   - Financial analytics and data visualization
   - Date-range filtering and trend analysis

4. **Technical Complexity**:
   - **Four interconnected Django models** with complex relationships (User -> Category -> Transaction/Budget/RecurringTransaction)
   - **RESTful API architecture** with full CRUD operations via JavaScript fetch
   - **Real-time chart updates** using Chart.js with dynamic data loading
   - **Automated transaction processing** for recurring bills with date calculations
   - **Budget tracking with period calculations** (weekly/monthly/yearly spending aggregation)
   - **Advanced filtering system** with date ranges, categories, transaction types, and search
   - **CSV export functionality** for data portability
   - **Mobile-responsive design** with collapsible sidebar navigation

## File Structure

### Backend (Python/Django)

- `financetracker/settings.py` - Django configuration with app settings, database, and security
- `financetracker/urls.py` - Main URL router including tracker app routes
- `tracker/models.py` - Database models:
  - `Category` - Income/expense categories with icons and colors
  - `Transaction` - Individual financial transactions
  - `Budget` - Spending limits per category with time periods
  - `RecurringTransaction` - Automated recurring bills/income
- `tracker/views.py` - View functions and API endpoints for all CRUD operations
- `tracker/urls.py` - URL patterns for tracker app
- `tracker/admin.py` - Django admin configuration for all models

### Frontend (Templates/JavaScript)

- `templates/tracker/base.html` - Base template with navigation, sidebar, and shared CSS/JS
- `templates/tracker/dashboard.html` - Main dashboard with statistics and Chart.js visualizations
- `templates/tracker/transactions.html` - Transaction list with filtering and CRUD modals
- `templates/tracker/budgets.html` - Budget management with progress tracking
- `templates/tracker/recurring.html` - Recurring transaction configuration
- `templates/tracker/categories.html` - Category management with color/icon customization
- `templates/tracker/login.html` - User login page
- `templates/tracker/register.html` - User registration page

## Features

### Dashboard
- Summary cards showing total income, expenses, and balance
- Interactive line chart comparing income vs expenses over time
- Doughnut chart showing expense distribution by category
- Recent transactions list
- Budget progress indicators
- Period selection (week/month/year)

### Transaction Management
- Add, edit, and delete transactions
- Categorize as income or expense
- Search and filter by date range, category, and type
- Autocomplete category selection

### Budget Tracking
- Create budgets for expense categories
- Track spending against budget limits
- Visual progress bars with color coding (green/yellow/red)
- Weekly, monthly, or yearly periods

### Recurring Transactions
- Set up automatic recurring transactions
- Support for daily, weekly, bi-weekly, monthly, yearly frequencies
- Automatic transaction creation on scheduled dates

### Categories
- Create custom income and expense categories
- Customize with colors and icons
- Default categories created on registration

### Data Export
- Export transactions to CSV format
- Filter by date range before export

## How to Run

1. **Install dependencies**:
   ```bash
   pip install django python-dateutil
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Start the development server**:
   ```bash
   python manage.py runserver 0.0.0.0:5000
   ```

4. **Access the application** at `http://localhost:5000`

5. **Create an account** to start tracking your finances

### Sample Data

To explore the dashboard with realistic numbers, load deterministic demo data:

```bash
python manage.py seed_sample_data --username demo --clear
```

This creates a `demo` account (password: `password123`), adds three months of transactions, budgets, and recurring items, and clears any existing data for that user when `--clear` is supplied.

## Requirements

- Python 3.8+
- Django 4.x+
- python-dateutil

All requirements are listed in `requirements.txt`.

## Additional Notes

- The application uses SQLite for simplicity but can be configured for PostgreSQL
- User authentication is handled by Django's built-in auth system
- All user data is private - users can only see their own transactions and budgets
- The frontend is fully responsive and works on mobile devices
- Charts update dynamically based on the selected time period
- CSRF protection is implemented for all API endpoints
