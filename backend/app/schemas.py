from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

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
    user_id: UUID

    class Config:
        from_attributes = True

class CreateUserProof(BaseModel):
    problem_id: int
    proof_text: str

class UserProofOutput(BaseModel):
    id: int
    problem_id: int
    proof_text: str
    verdict: Optional[str]
    confidence: Optional[float]
    submitted_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True
