from fastapi import APIRouter , Depends , HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user import UserModel
from app.schema.user import Register , Login
from app.security import hashPassword , verifyPassword , create_AcessToken
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/expense/auth")

@router.post("/login")
def login(data : Login , db:Annotated[Session , Depends(get_db)]):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verifyPassword(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_AcessToken({"sub": user.email})

    return {
        "message": "Logged in successfully",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@router.post("/register")
def register(data : Register , db:Annotated[Session , Depends(get_db)]):
    existing_user = db.query(UserModel).filter(data.email == UserModel.email).first()
    if  existing_user:
        return JSONResponse({"Message" : "User exists with the Email !!!!"}, status_code= 400)
    
    new_user = UserModel(
        name = data.name,
        email = data.email,
        password = hashPassword(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{
        "Message": "User is Created Successfully !!!",
        "item" : new_user
    }