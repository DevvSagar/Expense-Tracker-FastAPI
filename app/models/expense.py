from pydantic import BaseModel , Field


class Create_ExpenseTracker(BaseModel):
    title : str 
    amount: int
    category: str
    note: str 