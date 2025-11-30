import csv
import os
from datetime import datetime
from tabulate import tabulate

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "expenses.csv")


def _ensure_data_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "description", "amount"])


def add_expense():
    _ensure_data_file()

    date_str = input("Date (YYYY-MM-DD) [Enter for today]: ").strip()
    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format")
        return

    category = input("Category (food/travel/bills/other): ").strip() or "other"
    description = input("Description: ").strip() or "No description"

    amount_str = input("Amount (₹): ").strip()
    try:
        amount = float(amount_str)
    except ValueError:
        print("❌ Invalid amount")
        return

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, category, description, amount])

    print("✅ Expense Added")


def list_expenses(limit=None):
    _ensure_data_file()

    rows = []
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    if not rows:
        print("ℹ No expenses found")
        return

    if limit:
        rows = rows[-limit:]

    table = []
    for r in rows:
        table.append([r["date"], r["category"], r["description"], f"₹{r['amount']}"])

    print(tabulate(table, headers=["Date","Category","Description","Amount"], tablefmt="grid"))
