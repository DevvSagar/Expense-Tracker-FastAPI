from fastapi import APIRouter , Depends , HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.expense import ExpenseModel
from app.models.user import UserModel
from app.schema.expense import CreateExpense , UpdateExpense
from sqlalchemy import select , func
from app.dependencies import authenicate_user


router = APIRouter(prefix="/expense")

# Step 3 Get all details
@router.get("/")
def get_all(db:Annotated[Session,Depends(get_db)] , current_user: Annotated[dict,Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found !!")
    
    stmt = select(ExpenseModel.id , ExpenseModel.title , ExpenseModel.category , ExpenseModel.amount , ExpenseModel.note).filter(ExpenseModel.user_id == user.id)

    total = db.execute(stmt).mappings().all()
    return{ 
        "Message" : "This is Total list of Expenses !" ,
        "Total Expenses": total 
    }



# Step 3 — Test GET all Expense
@router.get("/get_expense")
def get_expenses(id: int,db:Annotated[Session,Depends(get_db)] , current_user : Annotated[dict , Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found !!")

    stmt = select(ExpenseModel.amount).filter(ExpenseModel.id == id).filter(ExpenseModel.user_id == user.id)
    amt = db.execute(stmt).mappings().all()
    return{
        "All_Amount " : amt
    }



# 1. Category filter ⭐ Easy - GET /expense/category/{category}

@router.get("/category/{category}")
def get_category(category : str , db:Annotated[Session,Depends(get_db)] , current_user: Annotated[dict,Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found !!")
    
    items = db.query(ExpenseModel).filter(ExpenseModel.category == category).where(ExpenseModel.user_id == user.id).all()
    if not items:
        raise HTTPException(status_code=404, detail="Category not found !!!")
    
    
    return{
        "Message" : "Here is expense according to given category .",
        "items" : items
    }



# Total expenses ⭐ Easy-Medium
# GET /expense/total

@router.get("/total")
def total_amount(db:Annotated[Session,Depends(get_db)] , current_user : Annotated[dict,Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404 , detail="User not Found !!")
    

    total_amount = db.query(func.sum(ExpenseModel.amount)).filter(ExpenseModel.user_id == user.id).scalar()
    if total_amount is None:
        return "Total Amount is 0"
    
    return{
        "Message": "Total Amount",
        "Amount": total_amount
    }

# Summary by category ⭐ Medium
# GET /expense/summary
@router.get("/summary")
def get_summary(db:Annotated[Session , Depends(get_db)] , current_user: Annotated[dict , Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404 , detail="User not Found !!")
    
    summary = db.query(ExpenseModel.category,func.sum(ExpenseModel.amount)).group_by(ExpenseModel.category).where(ExpenseModel.user_id == user.id).all()
    result = []

    for row in summary:
        result.append({
            "category": row[0],
            "total": row[1]
        })

    return{
        "Message" : "Here is your Total Epense per Category",
        "Summary": result
    }


@router.get("/{id}")
def getBy_id(id: int,db:Annotated[Session,Depends(get_db)] , current_user: Annotated[dict , Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404 , detail="User not Found !!")
    
    items = db.query(ExpenseModel).filter(ExpenseModel.id == id).filter(ExpenseModel.user_id == user.id).first()
    if not items:
        raise HTTPException(status_code=404, detail="Item not found !!!")
    
    return{
        "items": items
    }


@router.post("/")
def save_data(expense : CreateExpense , db : Annotated[Session, Depends(get_db)] , current_user: Annotated[dict,Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found !")
    
    data = ExpenseModel(title=expense.title , amount=expense.amount , category=expense.category , note=expense.note , user_id=user.id)
    db.add(data)
    db.commit()
    db.refresh(data)
    return{
        "Message" : "Expense Added",
        "item": data
    }





@router.put("/{id}")
def update(id: int ,update: UpdateExpense , db:Annotated[Session,Depends(get_db)] , current_user: Annotated[dict,Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found !")

    items = db.query(ExpenseModel).filter(ExpenseModel.id == id).filter(ExpenseModel.user_id == user.id).first()
    if not items:
        raise HTTPException(status_code=404, detail="Item not found !!!")

    if update.title is not None:
        items.title = update.title
    
    if update.amount is not None:
        items.amount = update.amount

    if update.category is not None:
        items.category = update.category

    if update.note is not None:
        items.note = update.note

    db.commit()
    db.refresh(items)
    return{
        "Message": "Expense item Updated", "update": items
    }
    

@router.delete("/{id}")
def delete(id: int , db : Annotated[Session , Depends(get_db)] , current_user: Annotated[dict,Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found !")
    
    items = db.query(ExpenseModel).filter(ExpenseModel.id == id).filter(ExpenseModel.user_id == user.id).first()
    if not items:
        raise HTTPException(status_code=404, detail="Item not found !!!")
    
    db.delete(items)
    db.commit()
    return{"Message": "Expense Deleted"}

