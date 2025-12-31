from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateProblem(BaseModel):
    problem_slug: str
    problem_title: str
    deadline: datetime
    difficulty: str

class ProblemOutput(BaseModel):
    id: int
    problem_slug: str
    problem_title: str
    deadline: datetime
    difficulty: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True