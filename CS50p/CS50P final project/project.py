import sqlite3
from datetime import datetime
from collections import defaultdict

DB_NAME = "expenses.db"


def main():
    """
    CLI entry point for the Expense Tracker.
    """
    initialize_db()

    print("📊 Smart Expense Tracker (SQLite)")
    print("1. Add Expense")
    print("2. Monthly Summary")
    print("3. Category Breakdown")

    choice = input("Choose an option (1-3): ").strip()

    if choice == "1":
        amount = float(input("Amount: "))
        category = input("Category: ").strip()
        date = input("Date (YYYY-MM-DD): ").strip()
        add_expense(amount, category, date)
        print("✅ Expense added successfully.")

    elif choice == "2":
        month = input("Enter month (YYYY-MM): ").strip()
        total = calculate_monthly_total(month)
        print(f"💰 Total expenses for {month}: {total}")

    elif choice == "3":
        month = input("Enter month (YYYY-MM): ").strip()
        breakdown = category_summary(month)
        print("📂 Category Breakdown:")
        for cat, amt in breakdown.items():
            print(f"{cat}: {amt}")

    else:
        print("❌ Invalid choice.")


def initialize_db():
    """
    Initializes the SQLite database and expenses table.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(amount, category, date):
    """
    Inserts a validated expense into the database.
    """
    validate_expense(amount, category, date)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (amount, category, date)
    )

    conn.commit()
    conn.close()


def calculate_monthly_total(month):
    """
    Calculates total expenses for a given month (YYYY-MM).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE date LIKE ?",
        (f"{month}%",)
    )

    result = cursor.fetchone()[0]
    conn.close()

    return round(result or 0.0, 2)


def category_summary(month):
    """
    Returns category-wise totals for a given month.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE date LIKE ?
        GROUP BY category
    """, (f"{month}%",))

    rows = cursor.fetchall()
    conn.close()

    return {category: round(total, 2) for category, total in rows}


def validate_expense(amount, category, date):
    """
    Validates expense inputs.
    """
    if amount <= 0:
        raise ValueError("Amount must be positive.")

    if not category:
        raise ValueError("Category cannot be empty.")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

def calculate_total_between_dates(start_date, end_date):
    validate_date_range(start_date, end_date)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM expenses
        WHERE date BETWEEN ? AND ?
        """,
        (start_date, end_date)
    )

    total = cursor.fetchone()[0]
    conn.close()

    return round(total or 0.0, 2)


def category_summary_between_dates(start_date, end_date):
    validate_date_range(start_date, end_date)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT category, SUM(amount)
        FROM expenses
        WHERE date BETWEEN ? AND ?
        GROUP BY category
        """,
        (start_date, end_date)
    )

    rows = cursor.fetchall()
    conn.close()

    return {category: round(total, 2) for category, total in rows}


def validate_date_range(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format.")

    if start > end:
        raise ValueError("Start date cannot be after end date.")

if __name__ == "__main__":
    main()
