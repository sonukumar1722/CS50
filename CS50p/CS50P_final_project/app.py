import streamlit as st
from datetime import date
from project import (
    initialize_db,
    add_expense,
    calculate_total_between_dates,
    category_summary_between_dates
)

initialize_db()

st.set_page_config(page_title="Smart Expense Tracker")

st.title("📊 Smart Expense Tracker")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Add Expense", "Date Range Summary", "Category Breakdown"]
)

# ---------------- ADD EXPENSE ----------------
if menu == "Add Expense":
    st.header("➕ Add Expense")

    amount = st.number_input("Amount", min_value=1.0)
    category = st.text_input("Category")
    expense_date = st.date_input("Date", value=date.today())

    if st.button("Save"):
        try:
            add_expense(amount, category, expense_date.strftime("%Y-%m-%d"))
            st.success("Expense added successfully")
        except Exception as e:
            st.error(str(e))

# ---------------- RANGE TOTAL ----------------
elif menu == "Date Range Summary":
    st.header("📅 Expense Summary")

    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Calculate"):
        try:
            total = calculate_total_between_dates(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            st.metric("Total Expenses", f"₹ {total}")
        except Exception as e:
            st.error(str(e))

# ---------------- CATEGORY SUMMARY ----------------
elif menu == "Category Breakdown":
    st.header("📂 Category Breakdown")

    start_date = st.date_input("Start Date", key="cat_start")
    end_date = st.date_input("End Date", key="cat_end")

    if st.button("Show"):
        try:
            summary = category_summary_between_dates(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )

            if summary:
                st.bar_chart(summary)
            else:
                st.warning("No data found in this range.")
        except Exception as e:
            st.error(str(e))
