from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from ..crud import category as crud_category
from .auth import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud_category.get_categories(db, current_user.id, skip, limit)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if category name already exists for this user
    existing = crud_category.get_category_by_name(db, category.name, current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Category name already exists")
    
    return crud_category.create_category(db, category, current_user.id)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = crud_category.get_category_by_id(db, category_id, current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = crud_category.update_category(db, category_id, current_user.id, category_update)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = crud_category.delete_category(db, category_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return None