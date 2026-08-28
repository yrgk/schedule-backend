from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response

from app.db import get_db
from app.models import Subject, SubjectScore


# Implementing router
router = APIRouter()


@router.get("/score")
def get_all_scores_handler(
    user_id: int,
    db: Session = Depends(get_db),
):
    # UPD: Validation with tg api hash
    if not user_id:
        return Response(status_code=401, content="Unauthorized")

    subject_scores = (
        db.query(SubjectScore, Subject.title.label("title"))
        .filter(SubjectScore.telegram_user_id == user_id)
        .join(Subject, Subject.id == SubjectScore.subject_id)
        .all()
    )

    return [{"score": score.score, "title": score.title} for score in subject_scores]


@router.get("/score/{subject_id}")
def get_score_handler(
    user_id: int,
    subject_id: int,
    db: Session = Depends(get_db),
):
    # UPD: Validation with tg api hash
    if not user_id:
        return Response(status_code=401, content="Unauthorized")

    subject_score = (
        db.query(SubjectScore, Subject.title.label("title"))
        .filter(SubjectScore.telegram_user_id == user_id)
        .filter(SubjectScore.subject_id == subject_id)
        .first()
    )

    if not subject_score:
        return Response(status_code=404, content="Not found")

    return {"score": subject_score.score}


@router.put("/score/{subject_id}")
def update_score_handler(
    score_delta: int,
    user_id: int,
    subject_id: int,
    is_increase: bool = True,
    db: Session = Depends(get_db),
):
    # UPD: Validation with tg api hash
    if not user_id:
        return Response(status_code=401, content="Unauthorized")

    subject_score = (
        db.query(SubjectScore)
        .filter(SubjectScore.telegram_user_id == user_id)
        .filter(SubjectScore.subject_id == subject_id)
        .first()
    )

    if not subject_score:
        return Response(status_code=404, content="Not found")

    # Calculate the new score based on the is_increase flag
    if is_increase:
        new_score = subject_score.score + score_delta
    else:
        new_score = subject_score.score - score_delta

    subject_score.score = new_score
    db.commit()
    db.refresh(subject_score)

    return {"score": subject_score.score}
