from fastapi import FastAPI, Depends
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.models import Problem
from app.routes import problems

from app import models
import os

app = FastAPI()
app.include_router(problems.router, prefix="/problems", tags=["problems"])

models.Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}


print("DB URL:", os.getenv("DATABASE_URL"))
print("App started successfully.")
