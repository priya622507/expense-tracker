# Expense Tracker (CSV)

A simple command-line expense tracker built in Python. All data is stored locally in a CSV file — no database or external dependencies required.

## Features

- **Add expenses** with date, category, description, and amount
- **View all expenses** in a clean, formatted table with running total
- **Filter expenses** by category or by date range
- **View summary** — total spending, breakdown by category, and breakdown by month
- **Delete an expense** by its ID
- **Persistent storage** — data is saved automatically to `expenses.csv`

## Requirements

- Python 3.6 or higher (no external libraries needed — uses only the standard library)

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/expense-tracker-csv.git
   cd expense-tracker-csv
   ```

2. Run the script:
   ```bash
   python expense_tracker.py
   ```

3. On first run, an `expenses.csv` file will be created automatically in the project folder to store your data.

## Usage

When you run the program, you'll see a menu:

```
========== EXPENSE TRACKER ==========
1. Add expense
2. View all expenses
3. Filter expenses
4. View summary
5. Delete an expense
6. Exit
======================================
```

Simply enter the number corresponding to the action you want to perform and follow the prompts.

### Example: Adding an expense
```
Date (YYYY-MM-DD) [press Enter for today]: 2026-07-10
Category (e.g., Food, Transport, Rent): Food
Description: Groceries
Amount: 45.50
```

## Data Format

Expenses are stored in `expenses.csv` with the following columns:

| Column      | Description                          |
|-------------|---------------------------------------|
| id          | Unique identifier for the expense     |
| date        | Date of the expense (YYYY-MM-DD)      |
| category    | Category label (e.g., Food, Rent)     |
| description | Short description of the expense      |
| amount      | Amount spent (numeric)                |

## Project Structure

```
expense-tracker-csv/
├── expense_tracker.py   # Main application script
├── expenses.csv          # Auto-generated data file (created on first run)
└── README.md             # Project documentation
```

## Notes

- It's recommended to add `expenses.csv` to your `.gitignore` file if you don't want your personal expense data included in version control.
- This project is intended as a lightweight, dependency-free tool for personal expense tracking and as a learning example for working with CSV files in Python.

## License

This project is open source and available for personal or educational use.
