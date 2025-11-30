import os
import pandas as pd

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "expenses.csv")


def load_expenses_dataframe() -> pd.DataFrame:
    """Load data from CSV as Pandas DataFrame"""
    if not os.path.exists(CSV_FILE):
        print("ℹ No expenses found. Add some expenses first.")
        return pd.DataFrame(columns=["date", "category", "description", "amount"])

    df = pd.read_csv(CSV_FILE)

    if df.empty:
        print("ℹ File is empty.")
        return df

    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    return df


def show_category_summary():
    df = load_expenses_dataframe()
    if df.empty:
        return

    summary = df.groupby("category")["amount"].sum().reset_index()
    print("\n📊 Category-wise Summary")
    print(summary.to_string(index=False))


def show_monthly_summary():
    df = load_expenses_dataframe()
    if df.empty:
        return

    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    summary = df.groupby("year_month")["amount"].sum().reset_index()

    print("\n📈 Month-wise Summary")
    print(summary.to_string(index=False))
