from sqlalchemy import ForeignKey,Integer,String,DateTime,Float
from sqlalchemy.orm import Mapped , mapped_column
from ..database.db import Base
from datetime import datetime, timezone

class ExpenseModel(Base):
    __tablename__ = "Expense_Tracker"

    id : Mapped[int] = mapped_column(Integer, primary_key=True , autoincrement=True, index=True )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    title : Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float,nullable=False)
    category: Mapped[str] = mapped_column(String)
    note: Mapped[str] = mapped_column(String, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at : Mapped[datetime] = mapped_column(DateTime,nullable=True,onupdate=lambda: datetime.now(timezone.utc))