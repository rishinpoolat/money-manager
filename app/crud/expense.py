from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from ..models.expense import Expense
from ..schemas.expense import ExpenseCreate, ExpenseUpdate
from datetime import datetime

def get_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Expense).filter(Expense.user_id == user_id).offset(skip).limit(limit).all()

def get_expense_by_id(db: Session, expense_id: int, user_id: int):
    return db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id
    ).first()

def get_expenses_by_category(db: Session, category_id: int, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Expense).filter(
        Expense.category_id == category_id,
        Expense.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_expenses_by_month(db: Session, user_id: int, year: int, month: int):
    return db.query(Expense).filter(
        Expense.user_id == user_id,
        extract('year', Expense.date) == year,
        extract('month', Expense.date) == month
    ).all()

def get_total_spent_by_category_month(db: Session, category_id: int, user_id: int, month: str):
    # month format: "YYYY-MM"
    year, month_num = month.split("-")
    
    total = db.query(func.sum(Expense.amount)).filter(
        Expense.category_id == category_id,
        Expense.user_id == user_id,
        extract('year', Expense.date) == int(year),
        extract('month', Expense.date) == int(month_num)
    ).scalar()
    
    return total or 0.0

def create_expense(db: Session, expense: ExpenseCreate, user_id: int):
    db_expense = Expense(**expense.dict(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def update_expense(db: Session, expense_id: int, user_id: int, expense_update: ExpenseUpdate):
    db_expense = get_expense_by_id(db, expense_id, user_id)
    if not db_expense:
        return None
    
    update_data = expense_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_expense, field, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int, user_id: int):
    db_expense = get_expense_by_id(db, expense_id, user_id)
    if db_expense:
        db.delete(db_expense)
        db.commit()
        return True
    return False