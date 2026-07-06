from fastapi import FastAPI
from app.routing import expense_route

app = FastAPI()

app.include_router(expense_route.router)