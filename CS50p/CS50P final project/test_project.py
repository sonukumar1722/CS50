import os
import pytest
from project import (
    initialize_db,
    add_expense,
    calculate_total_between_dates,
    category_summary_between_dates,
    validate_date_range,
    DB_NAME
)


@pytest.fixture(autouse=True)
def clean_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    initialize_db()
    yield
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)


def test_valid_date_range():
    validate_date_range("2024-05-01", "2024-05-31")


def test_invalid_date_range():
    with pytest.raises(ValueError):
        validate_date_range("2024-06-01", "2024-05-01")


def test_total_between_dates():
    add_expense(100, "Food", "2024-05-01")
    add_expense(200, "Travel", "2024-05-10")
    add_expense(50, "Food", "2024-06-01")

    total = calculate_total_between_dates("2024-05-01", "2024-05-31")
    assert total == 300.0


def test_category_summary_between_dates():
    add_expense(100, "Food", "2024-05-01")
    add_expense(50, "Food", "2024-05-02")
    add_expense(200, "Travel", "2024-05-03")

    summary = category_summary_between_dates("2024-05-01", "2024-05-31")

    assert summary["Food"] == 150.0
    assert summary["Travel"] == 200.0
