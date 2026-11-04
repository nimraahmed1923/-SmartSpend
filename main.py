
from datetime import datetime

from storage import load_data, save_data, EXPENSE_FILE, BUDGET_FILE


class ExpenseManager:
    def __init__(self):
        self.expenses = load_data(EXPENSE_FILE, [])
        self.budgets = load_data(BUDGET_FILE, {"default": 9000})

    def add_expense(self, title, amount, category, date):
        title = title.strip()
        category = category.strip()

        if not title or not category:
            raise ValueError("Title and category are required.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

        expense_id = max(
            (expense["id"] for expense in self.expenses),
            default=0
        ) + 1

        expense = {
            "id": expense_id,
            "title": title,
            "amount": round(amount, 2),
            "category": category,
            "date": date
        }

        self.expenses.append(expense)
        save_data(EXPENSE_FILE, self.expenses)

        return expense

    def view_expenses(self, month=None):
        if month is None:
            return self.expenses.copy()

        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            raise ValueError("Month must be in YYYY-MM format.")

        return [
            expense for expense in self.expenses
            if expense["date"].startswith(month)
        ]

    def edit_expense(self, expense_id, title, amount, category, date):
        title = title.strip()
        category = category.strip()

        if not title or not category:
            raise ValueError("Title and category are required.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

        for expense in self.expenses:
            if expense["id"] == expense_id:
                expense["title"] = title
                expense["amount"] = round(amount, 2)
                expense["category"] = category
                expense["date"] = date

                save_data(EXPENSE_FILE, self.expenses)

                return expense

        return None

    def delete_expense(self, expense_id):
        for expense in self.expenses:
            if expense["id"] == expense_id:
                self.expenses.remove(expense)
                save_data(EXPENSE_FILE, self.expenses)
                return True

        return False

    def get_budget(self, month):
        return self.budgets.get(
            month,
            self.budgets.get("default", 9000)
        )

    def set_budget(self, month, amount):
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            raise ValueError("Month must be in YYYY-MM format.")

        if amount <= 0:
            raise ValueError("Budget must be greater than zero.")

        self.budgets[month] = round(amount, 2)
        save_data(BUDGET_FILE, self.budgets)

        return self.budgets[month]

    def calculate_monthly_spending(self, month):
        expenses = self.view_expenses(month)

        return round(
            sum(expense["amount"] for expense in expenses),
            2
        )

    def calculate_remaining_budget(self, month):
        budget = self.get_budget(month)
        spending = self.calculate_monthly_spending(month)

        return round(budget - spending, 2)
