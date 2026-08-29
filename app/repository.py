import time

from sqlalchemy import or_
from sqlalchemy.orm import Session, load_only

from app.models import GroupToLesson, Lesson


def get_schedule_for_day(
    db: Session,
    group_id: int,
    study_week: int,  # Number of the study week, starting from 1 since beginning of the semester
    day_of_week: int | None = None,  # Day of the week, starting from 1 (Monday) to 7 (Sunday)
    is_odd_week: bool | None = None,
):
    if day_of_week is None:
        day_of_week = time.localtime().tm_wday + 1

    lessons = (
        db.query(Lesson)
        .options(
            load_only(
                Lesson.title,
                Lesson.day_of_week,
                Lesson.teacher_name,
                Lesson.start_time,
                Lesson.end_time,
                Lesson.location_short,
                Lesson.location,
            )
        )
        .join(GroupToLesson, GroupToLesson.lesson_id == Lesson.id)
        .filter(GroupToLesson.group_id == group_id)
        .filter(Lesson.day_of_week == day_of_week)
    )

    # Checking for odd/even week
    if is_odd_week is not None:
        lessons = lessons.filter(
            or_(
                Lesson.is_odd_week == is_odd_week,
                Lesson.is_odd_week.is_(None),
            )
        )

    # Checking study week range
    lessons = lessons.filter(
        or_(Lesson.start_week.is_(None), Lesson.start_week <= study_week),
        or_(Lesson.end_week.is_(None), Lesson.end_week >= study_week),
    )

    # Ordering lessons by start time and executing the query
    lessons = lessons.order_by(Lesson.start_time).all()

    if not lessons:
        return None

    return lessons
