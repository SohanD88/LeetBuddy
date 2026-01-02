from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, index=True)
    problem_title = Column(String, nullable=False)
    problem_slug = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)

class UserProof(Base):
    __tablename__ = "user_proofs"
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    proof_text = Column(String, nullable=False)  # e.g., "code", "screenshot"
    verdict = Column(String)
    confidence = Column(Float)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)