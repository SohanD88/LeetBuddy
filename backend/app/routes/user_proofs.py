from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserProof, Problem
from app.schemas import CreateUserProof, UserProofOutput
from app.verifier import verify_proof_text


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

@router.post("/verify/{proof_id}", response_model=UserProofOutput)
def verify_user_proof(proof_id: int, db: Session = Depends(get_db),):
    """
    Docstring for verify_user_proof
    
    Verifies the user proof with the given proof_id using AI
    1. Fetches the proof
    2. Calls verification
    3. Updates the proof with verdict and confidence
    4. Returns the updated proof
    """

    proof = db.query(UserProof).filter(UserProof.id == proof_id).first()
    if not proof:
        raise HTTPException(status_code = 404, detail = "User proof not found")
    
    verdict, confidence = verify_proof_text(proof.proof_text)
    proof.verdict = verdict
    proof.confidence = confidence

    problem = db.query(Problem).filter(Problem.id == proof.problem_id).first()

    if verdict == "pass":
        problem.status = "completed"
    
    else:
        problem.status = "failed"

    db.commit()
    db.refresh(proof)

    return proof