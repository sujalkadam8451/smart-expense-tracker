import os
import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "expenses.csv")


def _load_df() -> pd.DataFrame:
    """Load CSV into DataFrame"""
    if not os.path.exists(CSV_FILE):
        print("ℹ No expenses found. Add some first.")
        return pd.DataFrame(columns=["date", "category", "description", "amount"])

    df = pd.read_csv(CSV_FILE)

    if df.empty:
        print("ℹ No expenses to show.")
        return df

    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df


def plot_category_expenses():
    """Bar chart for category-wise expenses"""
    df = _load_df()
    if df.empty:
        return

    summary = df.groupby("category")["amount"].sum()

    plt.figure()
    summary.plot(kind="bar")
    plt.title("Category-wise Expenses")
    plt.xlabel("Category")
    plt.ylabel("Total Amount (₹)")
    plt.tight_layout()
    plt.show()


def plot_monthly_expenses():
    """Line chart for monthly expenses"""
    df = _load_df()
    if df.empty:
        return

    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    summary = df.groupby("year_month")["amount"].sum()

    plt.figure()
    summary.plot(kind="line", marker="o")
    plt.title("Month-wise Expenses")
    plt.xlabel("Month")
    plt.ylabel("Total Amount (₹)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
