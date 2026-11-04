
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from main import ExpenseManager


app = FastAPI(title="SmartSpend API")
manager = ExpenseManager()


class ExpenseInput(BaseModel):
    title: str
    amount: float = Field(gt=0)
    category: str
    date: str


class BudgetInput(BaseModel):
    month: str
    monthly_budget: float = Field(gt=0)


@app.get("/")
def home():
    return {"message": "Welcome to SmartSpend API"}


@app.post("/expenses")
def add_expense(expense: ExpenseInput):
    try:
        return manager.add_expense(
            expense.title,
            expense.amount,
            expense.category,
            expense.date
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.get("/expenses")
def view_expenses(month: str = None):
    try:
        return manager.view_expenses(month)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.put("/expenses/{expense_id}")
def edit_expense(expense_id: int, expense: ExpenseInput):
    try:
        updated_expense = manager.edit_expense(
            expense_id,
            expense.title,
            expense.amount,
            expense.category,
            expense.date
        )

        if updated_expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        return updated_expense

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    if manager.delete_expense(expense_id):
        return {"message": "Expense deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


@app.get("/budget")
def get_budget(month: str):
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Month must be in YYYY-MM format."
        )

    return {
        "month": month,
        "monthly_budget": manager.get_budget(month),
        "total_spending": manager.calculate_monthly_spending(month),
        "remaining_budget": manager.calculate_remaining_budget(month)
    }


@app.put("/budget")
def update_budget(budget: BudgetInput):
    try:
        amount = manager.set_budget(
            budget.month,
            budget.monthly_budget
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "message": "Monthly budget updated successfully",
        "month": budget.month,
        "monthly_budget": amount
    }
