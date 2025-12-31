from fastapi import FastAPI, Depends
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.models import Problem
from app.routes import problems
from app.routes import user_proofs


from app import models
import os

app = FastAPI()
app.include_router(problems.router, prefix="/problems", tags=["problems"])
app.include_router(user_proofs.router, prefix="/user_proofs", tags=["user_proofs"])

models.Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}


print("DB URL:", os.getenv("DATABASE_URL"))
print("App started successfully.")
