from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import Problem

def check_overdue_problems(db: Session) -> int:
    """
    Finds problems that are overdue and updates their status to 'failed'.
    Returns the number of problems updated.
    """

    current = datetime.now(timezone.utc)

    overdue_problems = (
        db.query(Problem)
        .filter(Problem.deadline != None)
        .filter(Problem.deadline < current)
        .filter(Problem.status == "pending")
        .filter(Problem.user_id != None)
        .all()
    )

    for problem in overdue_problems:
        problem.status = "failed"

    db.commit()
    return len(overdue_problems)
