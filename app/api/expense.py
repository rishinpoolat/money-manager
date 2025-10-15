from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from ..crud import expense as crud_expense
from ..crud import category as crud_category
from ..crud import budget as crud_budget
from ..models.user import User
from ..utils.email import send_budget_exceeded_email, send_budget_warning_email
from .auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud_expense.get_expenses(db, current_user.id, skip, limit)

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify category belongs to user
    category = crud_category.get_category_by_id(db, expense.category_id, current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Create the expense
    db_expense = crud_expense.create_expense(db, expense, current_user.id)
    
    # Check if budget exists and send notifications
    current_month = datetime.now().strftime("%Y-%m")
    budget = crud_budget.get_budget_by_category(db, expense.category_id, current_month, current_user.id)
    
    if budget:
        total_spent = crud_expense.get_total_spent_by_category_month(
            db, expense.category_id, current_user.id, current_month
        )
        
        percentage = (total_spent / budget.amount) * 100 if budget.amount > 0 else 0
        
        # Send warning at 80% (and only once - between 80-99%)
        if 80 <= percentage < 100:
            try:
                send_budget_warning_email(
                    to_email=current_user.email,
                    category_name=category.name,
                    budget_amount=budget.amount,
                    spent_amount=total_spent
                )
            except Exception as e:
                print(f"Failed to send warning email: {e}")
        
        # Send alert when exceeded
        elif total_spent > budget.amount:
            try:
                send_budget_exceeded_email(
                    to_email=current_user.email,
                    category_name=category.name,
                    budget_amount=budget.amount,
                    spent_amount=total_spent
                )
            except Exception as e:
                print(f"Failed to send email: {e}")
    
    return db_expense

@router.get("/report/{year}/{month}")
def get_monthly_report(
    year: int,
    month: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed monthly expense report"""
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month")
    
    expenses = crud_expense.get_expenses_by_month(db, current_user.id, year, month)
    
    # Group by category
    category_totals = {}
    for expense in expenses:
        category = crud_category.get_category_by_id(db, expense.category_id, current_user.id)
        if category.name not in category_totals:
            category_totals[category.name] = 0
        category_totals[category.name] += expense.amount
    
    total_spent = sum(category_totals.values())
    
    return {
        "month": f"{year}-{month:02d}",
        "total_expenses": len(expenses),
        "total_spent": total_spent,
        "monthly_income": current_user.monthly_income,
        "savings": current_user.monthly_income - total_spent,
        "savings_percentage": ((current_user.monthly_income - total_spent) / current_user.monthly_income * 100) if current_user.monthly_income > 0 else 0,
        "by_category": category_totals
    }

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = crud_expense.get_expense_by_id(db, expense_id, current_user.id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.get("/category/{category_id}", response_model=List[ExpenseResponse])
def get_expenses_by_category(
    category_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify category belongs to user
    category = crud_category.get_category_by_id(db, category_id, current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return crud_expense.get_expenses_by_category(db, category_id, current_user.id, skip, limit)

@router.get("/month/{year}/{month}", response_model=List[ExpenseResponse])
def get_expenses_by_month(
    year: int,
    month: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month")
    
    return crud_expense.get_expenses_by_month(db, current_user.id, year, month)

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # If category is being updated, verify it belongs to user
    if expense_update.category_id:
        category = crud_category.get_category_by_id(db, expense_update.category_id, current_user.id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    expense = crud_expense.update_expense(db, expense_id, current_user.id, expense_update)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = crud_expense.delete_expense(db, expense_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return None
