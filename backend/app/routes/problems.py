from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Problem
from app.schemas import CreateProblem, ProblemOutput
from app.deadlines import check_overdue_problems
from app.auth import get_current_user_id
from fastapi import HTTPException


router = APIRouter()

@router.post("/", response_model=ProblemOutput)
def create_problem(problem: CreateProblem, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    new_problem = Problem(
        problem_slug=problem.problem_slug,
        problem_title=problem.problem_title,
        deadline=problem.deadline,
        difficulty=problem.difficulty,
        status="pending",
        user_id=user_id
    )

    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)

    return new_problem

@router.get("/current", response_model = ProblemOutput)
def get_current_problem(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    problem = (
        db.query(Problem)
        .filter(Problem.user_id == user_id)
        .filter(Problem.status == "pending")
        .order_by(Problem.created_at.desc())
        .first()
    )
    if not problem:
        raise HTTPException(status_code=404, detail="No current problem found")

    return problem


@router.post("/check-deadlines")
def check_deadlines(db: Session = Depends(get_db)):
    """
    Manaully triggering the deadline checker
    V2 will likelt use cron and schedule it
    """
    updated_count = check_overdue_problems(db)
    return {"message": "Checked deadlines", "problems_failed": updated_count}