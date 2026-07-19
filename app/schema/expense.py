from pydantic import BaseModel, Field
from typing import Optional

class CreateExpense(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=2, max_length=50)
    note: Optional[str] = None

class UpdateExpense(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    amount: float | None = Field(default=None, gt=0)
    category: str | None = Field(default=None, min_length=2, max_length=50)
    note: str | None = None





