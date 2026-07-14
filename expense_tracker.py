#!/usr/bin/env python3
"""
Expense Tracker (CSV-based)
----------------------------
A simple command-line expense tracker that stores all data in a CSV file.

Features:
  1. Add an expense (date, category, description, amount)
  2. View all expenses
  3. Filter expenses by category or date range
  4. View summary (total spend, spend by category, monthly totals)
  5. Delete an expense by ID
  6. Data persists in 'expenses.csv' in the same folder as this script

Run:
    python expense_tracker.py
"""

import csv
import os
from datetime import datetime

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.csv")
FIELDNAMES = ["id", "date", "category", "description", "amount"]


# ----------------------------- Core CSV Helpers ----------------------------- #

def init_csv():
    """Create the CSV file with headers if it doesn't already exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_all_expenses():
    """Return a list of dicts, one per expense row."""
    init_csv()
    with open(CSV_FILE, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_all_expenses(expenses):
    """Overwrite the CSV file with the given list of expense dicts."""
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(expenses)


def get_next_id(expenses):
    if not expenses:
        return 1
    return max(int(e["id"]) for e in expenses) + 1


# ----------------------------- Validation Helpers ----------------------------- #

def prompt_date():
    while True:
        raw = input("Date (YYYY-MM-DD) [press Enter for today]: ").strip()
        if raw == "":
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("  Invalid date format. Please use YYYY-MM-DD.")


def prompt_amount():
    while True:
        raw = input("Amount: ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("  Amount must be positive.")
                continue
            return round(amount, 2)
        except ValueError:
            print("  Invalid amount. Please enter a number (e.g., 12.50).")


# ----------------------------- Feature Functions ----------------------------- #

def add_expense():
    print("\n--- Add New Expense ---")
    expenses = read_all_expenses()
    new_id = get_next_id(expenses)
    date = prompt_date()
    category = input("Category (e.g., Food, Transport, Rent): ").strip() or "Uncategorized"
    description = input("Description: ").strip() or "-"
    amount = prompt_amount()

    new_expense = {
        "id": new_id,
        "date": date,
        "category": category,
        "description": description,
        "amount": amount,
    }

    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(new_expense)

    print(f"✔ Expense #{new_id} added successfully.\n")


def display_expenses(expenses):
    if not expenses:
        print("No expenses found.\n")
        return

    print(f"\n{'ID':<5}{'Date':<12}{'Category':<15}{'Description':<25}{'Amount':>10}")
    print("-" * 67)
    total = 0.0
    for e in expenses:
        amount = float(e["amount"])
        total += amount
        print(f"{e['id']:<5}{e['date']:<12}{e['category']:<15}{e['description'][:24]:<25}{amount:>10.2f}")
    print("-" * 67)
    print(f"{'TOTAL':<57}{total:>10.2f}\n")


def view_all_expenses():
    print("\n--- All Expenses ---")
    expenses = read_all_expenses()
    display_expenses(expenses)


def filter_expenses():
    print("\n--- Filter Expenses ---")
    print("1. By category")
    print("2. By date range")
    choice = input("Choose filter type (1-2): ").strip()

    expenses = read_all_expenses()

    if choice == "1":
        category = input("Enter category to filter by: ").strip().lower()
        filtered = [e for e in expenses if e["category"].lower() == category]
    elif choice == "2":
        start = input("Start date (YYYY-MM-DD): ").strip()
        end = input("End date (YYYY-MM-DD): ").strip()
        try:
            start_dt = datetime.strptime(start, "%Y-%m-%d")
            end_dt = datetime.strptime(end, "%Y-%m-%d")
            filtered = [
                e for e in expenses
                if start_dt <= datetime.strptime(e["date"], "%Y-%m-%d") <= end_dt
            ]
        except ValueError:
            print("Invalid date format.\n")
            return
    else:
        print("Invalid choice.\n")
        return

    display_expenses(filtered)


def view_summary():
    print("\n--- Expense Summary ---")
    expenses = read_all_expenses()
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    total = sum(float(e["amount"]) for e in expenses)
    print(f"Total spending: {total:.2f}\n")

    # By category
    by_category = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + float(e["amount"])

    print("Spending by Category:")
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {cat:<20}{amt:>10.2f}")

    # By month
    by_month = {}
    for e in expenses:
        month = e["date"][:7]  # YYYY-MM
        by_month[month] = by_month.get(month, 0) + float(e["amount"])

    print("\nSpending by Month:")
    for month, amt in sorted(by_month.items()):
        print(f"  {month:<20}{amt:>10.2f}")
    print()


def delete_expense():
    print("\n--- Delete an Expense ---")
    expenses = read_all_expenses()
    if not expenses:
        print("No expenses to delete.\n")
        return

    display_expenses(expenses)
    target_id = input("Enter the ID of the expense to delete: ").strip()

    remaining = [e for e in expenses if e["id"] != target_id]
    if len(remaining) == len(expenses):
        print(f"No expense found with ID {target_id}.\n")
        return

    write_all_expenses(remaining)
    print(f"✔ Expense #{target_id} deleted.\n")


# ----------------------------- Main Menu ----------------------------- #

def main_menu():
    init_csv()
    menu = """
========== EXPENSE TRACKER ==========
1. Add expense
2. View all expenses
3. Filter expenses
4. View summary
5. Delete an expense
6. Exit
======================================
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all_expenses()
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            view_summary()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Goodbye! Your data is saved in expenses.csv")
            break
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main_menu()
