from expense_manager import add_expense, list_expenses
from analytics import show_category_summary, show_monthly_summary
from visualize import plot_category_expenses, plot_monthly_expenses


def print_menu():
    print("\n" + "=" * 40)
    print("      💰 Smart Expense Tracker 💰")
    print("=" * 40)
    print("1. Add new expense")
    print("2. View recent expenses")
    print("3. Category-wise summary")
    print("4. Month-wise summary")
    print("5. Show category-wise chart")
    print("6. Show month-wise chart")
    print("0. Exit")
    print("=" * 40)


def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            limit_input = input("How many recent records? (Blank = all): ").strip()
            limit = int(limit_input) if limit_input else None
            list_expenses(limit)

        elif choice == "3":
            show_category_summary()

        elif choice == "4":
            show_monthly_summary()

        elif choice == "5":
            plot_category_expenses()

        elif choice == "6":
            plot_monthly_expenses()

        elif choice == "0":
            print("👋 Thank you for using Expense Tracker!")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
