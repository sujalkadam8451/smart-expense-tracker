import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
import builtins

from expense_manager import add_expense
from analytics import load_expenses_dataframe
from visualize import plot_category_expenses, plot_monthly_expenses

# ------------- GLOBAL THEME -------------
ctk.set_appearance_mode("dark")          # dark / light / system
ctk.set_default_color_theme("dark-blue") # blue / green / dark-blue

# ------------- MAIN WINDOW -------------
app = ctk.CTk()
app.title("Smart Expense Tracker – Neon Dashboard")
app.geometry("1100x650")
app.minsize(1000, 600)

# layout weight so it resizes nicely
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# ------------- SIDEBAR -------------
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.grid(row=0, column=0, sticky="nsw")

logo = ctk.CTkLabel(
    sidebar,
    text="💰 Expense\nTracker",
    font=("Poppins", 24, "bold"),
    justify="left"
)
logo.pack(pady=(30, 10), padx=20, anchor="w")

tagline = ctk.CTkLabel(
    sidebar,
    text="Track • Analyze • Visualize",
    font=("Poppins", 12)
)
tagline.pack(padx=20, anchor="w", pady=(0, 20))


def nav_button(text, command):
    return ctk.CTkButton(
        sidebar,
        text=text,
        font=("Poppins", 15),
        height=42,
        corner_radius=12,
        fg_color="#1f4b99",
        hover_color="#295fcc",
        command=command
    )


# ------------- MAIN CONTENT AREA -------------
main_frame = ctk.CTkFrame(app, corner_radius=20)
main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
main_frame.grid_rowconfigure(2, weight=1)
main_frame.grid_columnconfigure(0, weight=1)


# ------------- HELPER: CLEAR MAIN -------------
def clear_main():
    for w in main_frame.winfo_children():
        w.destroy()


# ------------- DASHBOARD STATS -------------
def get_dashboard_stats():
    df = load_expenses_dataframe()
    if df.empty:
        return {
            "Total Spent (₹)": "0",
            "Total Records": "0",
            "Categories": "0",
            "Last Entry": "—"
        }

    total_spent = df["amount"].sum()
    total_records = len(df)
    total_categories = df["category"].nunique()
    last_date = df["date"].max().strftime("%Y-%m-%d")

    return {
        "Total Spent (₹)": f"{total_spent:.2f}",
        "Total Records": str(total_records),
        "Categories": str(total_categories),
        "Last Entry": last_date
    }


def create_stat_card(parent, title, value, emoji):
    card = ctk.CTkFrame(parent, corner_radius=18)
    card.pack(side="left", expand=True, fill="both", padx=10)

    icon = ctk.CTkLabel(card, text=emoji, font=("Poppins", 26))
    icon.pack(anchor="w", padx=15, pady=(12, 0))

    lbl_title = ctk.CTkLabel(card, text=title, font=("Poppins", 13))
    lbl_title.pack(anchor="w", padx=15, pady=(2, 0))

    lbl_value = ctk.CTkLabel(card, text=value, font=("Poppins", 20, "bold"))
    lbl_value.pack(anchor="w", padx=15, pady=(2, 12))


# ------------- SUMMARY TABLE VIEW -------------
def show_summary_in_gui(df, title_text):
    clear_main()

    header = ctk.CTkLabel(
        main_frame,
        text=title_text,
        font=("Poppins", 26, "bold")
    )
    header.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 5))

    sub = ctk.CTkLabel(
        main_frame,
        text="Insights based on your expense history",
        font=("Poppins", 12)
    )
    sub.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

    if df.empty:
        ctk.CTkLabel(
            main_frame,
            text="No data found. Add some expenses first.",
            font=("Poppins", 14)
        ).grid(row=2, column=0, padx=20, pady=20, sticky="nw")
        return

    table_frame = ctk.CTkFrame(main_frame, corner_radius=16)
    table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    # headers
    for col, column_name in enumerate(df.columns):
        h = ctk.CTkLabel(
            table_frame,
            text=column_name,
            font=("Poppins", 15, "bold")
        )
        h.grid(row=0, column=col, padx=10, pady=10, sticky="w")

    # rows
    for r_i, row in df.iterrows():
        for c_i, value in enumerate(row):
            cell = ctk.CTkLabel(
                table_frame,
                text=str(value),
                font=("Poppins", 13)
            )
            cell.grid(row=r_i + 1, column=c_i, padx=10, pady=4, sticky="w")


# ------------- CATEGORY SUMMARY -------------
def category_summary_gui():
    df = load_expenses_dataframe()
    if df.empty:
        show_summary_in_gui(df, "Category Summary")
        return

    summary = df.groupby("category")["amount"].sum().reset_index()
    show_summary_in_gui(summary, "Category Summary")


# ------------- MONTHLY SUMMARY -------------
def monthly_summary_gui():
    df = load_expenses_dataframe()
    if df.empty:
        show_summary_in_gui(df, "Monthly Summary")
        return

    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    summary = df.groupby("year_month")["amount"].sum().reset_index()
    show_summary_in_gui(summary, "Monthly Summary")


# ------------- HOME / DASHBOARD VIEW -------------
def show_home():
    clear_main()

    # top bar
    top_bar = ctk.CTkFrame(main_frame, height=80, corner_radius=18)
    top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 10))
    top_bar.grid_columnconfigure(0, weight=1)

    welcome = ctk.CTkLabel(
        top_bar,
        text="Dashboard Overview",
        font=("Poppins", 22, "bold")
    )
    welcome.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 0))

    subtitle = ctk.CTkLabel(
        top_bar,
        text="Quick glance at your spending and add new expenses.",
        font=("Poppins", 12)
    )
    subtitle.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

    # stats row
    stats_frame = ctk.CTkFrame(main_frame, corner_radius=18)
    stats_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
    stats_frame.pack_propagate(False)

    stats = get_dashboard_stats()

    create_stat_card(stats_frame, "Total Spent (₹)", stats["Total Spent (₹)"], "💳")
    create_stat_card(stats_frame, "Total Records", stats["Total Records"], "📂")
    create_stat_card(stats_frame, "Categories", stats["Categories"], "🧾")
    create_stat_card(stats_frame, "Last Entry", stats["Last Entry"], "📅")

    # form area
    form_wrapper = ctk.CTkFrame(main_frame, corner_radius=18)
    form_wrapper.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 10))
    form_wrapper.grid_columnconfigure(1, weight=1)

    form_title = ctk.CTkLabel(
        form_wrapper,
        text="Add New Expense",
        font=("Poppins", 18, "bold")
    )
    form_title.grid(row=0, column=0, columnspan=2, sticky="w",
                    padx=20, pady=(15, 5))

    caption = ctk.CTkLabel(
        form_wrapper,
        text="Fill the details below and record your transaction.",
        font=("Poppins", 11)
    )
    caption.grid(row=1, column=0, columnspan=2, sticky="w",
                 padx=20, pady=(0, 10))

    # fields
    labels_entries = [
        ("Date (YYYY-MM-DD)", "YYYY-MM-DD"),
        ("Category", "Food / Travel / Bills"),
        ("Description", "Short note about expense"),
        ("Amount (₹)", "Amount in rupees"),
    ]

    entries = []

    for i, (label_text, placeholder) in enumerate(labels_entries, start=2):
        lbl = ctk.CTkLabel(form_wrapper, text=label_text,
                           font=("Poppins", 13))
        lbl.grid(row=i, column=0, sticky="w", padx=20, pady=8)

        ent = ctk.CTkEntry(
            form_wrapper,
            placeholder_text=placeholder,
            height=36,
            corner_radius=10
        )
        ent.grid(row=i, column=1, sticky="ew", padx=20, pady=8)
        entries.append(ent)

    date_entry, cat_entry, desc_entry, amt_entry = entries

    # add button
    def add_data():
        date = date_entry.get()
        cat = cat_entry.get()
        desc = desc_entry.get()
        amt = amt_entry.get()

        if not date or not cat or not desc or not amt:
            messagebox.showerror("Error", "All fields are required.")
            return

        old_input = builtins.input
        builtins.input = lambda p="": {
            "Date (YYYY-MM-DD) [Enter for today]: ": date,
            "Category (food/travel/bills/other): ": cat,
            "Description: ": desc,
            "Amount (₹): ": amt
        }.get(p, "")

        add_expense()
        builtins.input = old_input

        messagebox.showinfo("Success", "Expense added successfully ✅")

        # clear fields
        date_entry.delete(0, "end")
        cat_entry.delete(0, "end")
        desc_entry.delete(0, "end")
        amt_entry.delete(0, "end")

        # refresh stats
        show_home()

    add_btn = ctk.CTkButton(
        form_wrapper,
        text="➕ Save Expense",
        font=("Poppins", 16, "bold"),
        height=44,
        corner_radius=14,
        fg_color="#22c55e",
        hover_color="#16a34a",
        command=add_data
    )
    add_btn.grid(row=len(labels_entries) + 2, column=0,
                 columnspan=2, pady=20, padx=20, sticky="e")


# ------------- NAV BUTTONS (after functions defined) -------------
btn_home = nav_button("🏠 Dashboard", show_home)
btn_home.pack(pady=8, fill="x", padx=15)

btn_summary = nav_button("📊 Category Summary", category_summary_gui)
btn_summary.pack(pady=8, fill="x", padx=15)

btn_monthly = nav_button("📈 Monthly Summary", monthly_summary_gui)
btn_monthly.pack(pady=8, fill="x", padx=15)

btn_cchart = nav_button("📌 Category Chart", plot_category_expenses)
btn_cchart.pack(pady=8, fill="x", padx=15)

btn_mchart = nav_button("📌 Monthly Chart", plot_monthly_expenses)
btn_mchart.pack(pady=8, fill="x", padx=15)

# filler at bottom
ctk.CTkLabel(
    sidebar,
    text="v1.0 • Python + CustomTkinter",
    font=("Poppins", 10)
).pack(side="bottom", pady=15)


# ------------- START -------------
show_home()
app.mainloop()
