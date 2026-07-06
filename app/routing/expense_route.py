from fastapi import APIRouter , Depends , HTTPException
from typing import Annotated


router = APIRouter(prefix="/expense")

@router.get("/")
def root():
    return{ "Message" : "This is our route !!" }