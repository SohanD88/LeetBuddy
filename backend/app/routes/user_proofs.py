from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserProof, Problem
from app.schemas import CreateUserProof, UserProofOutput

router = APIRouter()
@router.post("/", response_model=UserProofOutput)
def submit_user_proof(proof: CreateUserProof, db: Session = Depends(get_db),):
    problem = db.query(Problem).filter(Problem.id == proof.problem_id).first()
    if not problem:
        raise HTTPException(status_code = 404, detail = "Problem not found")
    
    new_proof = UserProof(
        problem_id=proof.problem_id,
        proof_text=proof.proof_text,
        verdict = None,
        confidence = None
    )

    db.add(new_proof)
    db.commit()
    db.refresh(new_proof)

    return new_proof