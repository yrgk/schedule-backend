from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Group
from app.repository import get_schedule_for_day
from app.schemas import LessonResponse
from app.time_service import (
    categorize_schedule,
    get_study_week,
    is_before_semester_start,
    is_odd_study_week,
    parse_schedule_date,
)


# Implementing router
router = APIRouter()


@router.get("/groups")
async def get_groups_handler(db: Session = Depends(get_db)):
    groups = db.query(Group).order_by(Group.name).all()
    return [{"id": group.id, "name": group.name} for group in groups]


@router.get("/{group_id}")
async def get_schedule_handler(
    group_id: int,
    day: str | None = Query(default=None, examples=["25.08.2026"]),
    with_time: bool = False,
    db: Session = Depends(get_db),
):
    # Parsing day in date format
    schedule_date = parse_schedule_date(day)

    # Checking if the date is before the semester start
    if is_before_semester_start(schedule_date):
        return Response(status_code=404, content="Not found")

    # Parsing day of week in data format
    day_of_week = schedule_date.weekday() + 1

    # Getting number of the study week
    study_week = get_study_week(schedule_date)

    # Checking if the study week is odd or even
    is_odd_week = is_odd_study_week(schedule_date)


    # Fetching schedule from the database
    schedule = get_schedule_for_day(
        db=db,
        group_id=group_id,
        study_week=study_week,
        day_of_week=day_of_week,
        is_odd_week=is_odd_week,
    )

    if not schedule:
        return Response(status_code=404, content="Not found")

    try:
        schedule_response = [
            LessonResponse(
                title=lesson.title,
                start_time=lesson.start_time,
                end_time=lesson.end_time,
                teacher_name=lesson.teacher_name,
                location_short=lesson.location_short,
                location=lesson.location,
            )
            for lesson in schedule
        ]
        if with_time:
            return categorize_schedule(schedule_response, schedule_date)
        return schedule_response

    except Exception as e:
        return Response(status_code=500, content=f"Error {e}")
