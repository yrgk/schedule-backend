from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.db import get_db
from app.repository import get_schedule_for_day
from app.schemas import LessonResponse
from app.time_service import (
    categorize_schedule,
    get_study_week,
    is_odd_study_week,
    parse_schedule_date,
)


# Implementing router
router = APIRouter()


@router.get("/{group_id}")
async def get_schedule_handler(
    group_id: str,
    day: str | None = Query(default=None, examples=["25.08.2026"]),
    with_time: bool = False,
    db: Session = Depends(get_db),
):
    # Parsing day of week in data format
    schedule_date = parse_schedule_date(day)
    day_of_week = schedule_date.weekday() + 1

    study_week = get_study_week(schedule_date)
    is_odd_week = is_odd_study_week(schedule_date)
    schedule = get_schedule_for_day(
        db,
        group_id,
        day_of_week,
        is_odd_week,
        study_week,
    )

    if not schedule:
        return Response(status_code=404, content="Not found")

    try:
        schedule_response = [
            LessonResponse(
                **{
                    **lesson[0].__dict__,
                    "title": lesson[1],
                    "teacher_name": lesson[2],
                }
            )
            for lesson in schedule
        ]
        if with_time:
            return categorize_schedule(schedule_response, schedule_date)
        return schedule_response

    except Exception as e:
        return Response(status_code=500, content=f"Error {e}")
