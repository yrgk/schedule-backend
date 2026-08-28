import time

from sqlalchemy import or_
from sqlalchemy.orm import Session, load_only

from app.models import Lesson, Subject


def get_schedule_for_day(
    db: Session,
    group_id: int,
    day: int | None = None,
    is_odd_week: bool | None = None,
    study_week: int | None = None,
):
    if day is None:
        day = time.localtime().tm_wday + 1

    lessons = (
        db.query(
            Lesson,
            Subject.title.label("title"),
        )
        .options(
            load_only(
                Lesson.day_of_week,
                Lesson.teacher_name,
                Lesson.start_time,
                Lesson.end_time,
                Lesson.location_short,
                Lesson.location,
                Lesson.subject_id,
                Lesson.group_id,
            )
        )
        .join(Subject, Lesson.subject_id == Subject.id)
        .filter(Lesson.group_id == group_id)
        .filter(Lesson.day_of_week == day)
    )

    if is_odd_week is not None:
        lessons = lessons.filter(
            or_(
                Lesson.is_odd_week == is_odd_week,
                Lesson.is_odd_week.is_(None),
            )
        )

    if study_week is not None:
        lessons = lessons.filter(
            or_(Lesson.start_week.is_(None), Lesson.start_week <= study_week),
            or_(Lesson.end_week.is_(None), Lesson.end_week >= study_week),
        )

    lessons = lessons.order_by(Lesson.start_time).all()

    if not lessons:
        return None

    return lessons
