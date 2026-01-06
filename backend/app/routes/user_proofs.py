from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserProof, Problem
from app.schemas import CreateUserProof, UserProofOutput
from app.verifier import verify_proof_text
from app.auth import get_current_user_id
from app.utils.hash import compute_hash


router = APIRouter()
@router.post("/", response_model=UserProofOutput)
def submit_user_proof(
    proof: CreateUserProof,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    problem = (
        db.query(Problem)
        .filter(Problem.id == proof.problem_id)
        .filter(Problem.user_id == user_id)
        .first()
    )
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    if not proof.proof_text:
        raise HTTPException(
            status_code=400,
            detail="Proof text is required for this proof type"
        )

    proof_hash = compute_hash(proof.proof_text)

    existing_proof = (
        db.query(UserProof)
        .filter(UserProof.proof_hash == proof_hash)
        .first()
    )
    if existing_proof:
        raise HTTPException(
            status_code=400,
            detail="This proof has already been submitted"
        )

    new_proof = UserProof(
        problem_id=proof.problem_id,
        proof_type=proof.proof_type,
        proof_text=proof.proof_text,
        proof_hash=proof_hash,
        proof_metadata=None,
        verdict=None,
        confidence=None,
        user_id=user_id,
    )

    db.add(new_proof)
    db.commit()
    db.refresh(new_proof)

    return new_proof

@router.post("/verify/{proof_id}", response_model=UserProofOutput)
def verify_user_proof(proof_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """
    Docstring for verify_user_proof
    
    Verifies the user proof with the given proof_id using AI
    1. Fetches the proof
    2. Calls verification
    3. Updates the proof with verdict and confidence
    4. Returns the updated proof
    """

    proof = db.query(UserProof).filter(UserProof.id == proof_id).filter(UserProof.user_id == user_id).first()
    if not proof:
        raise HTTPException(status_code = 404, detail = "User proof not found")
    
    verdict, confidence = verify_proof_text(proof.proof_text)
    proof.verdict = verdict
    proof.confidence = confidence

    problem = db.query(Problem).filter(Problem.id == proof.problem_id).filter(Problem.user_id == user_id).first()

    if verdict == "pass":
        problem.status = "completed"
    
    else:
        problem.status = "failed"

    db.commit()
    db.refresh(proof)

    return proof