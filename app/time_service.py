from datetime import date, datetime, timedelta

from fastapi import HTTPException

from app.config import Settings
from app.schemas import LessonResponse


def parse_schedule_date(day: str | None) -> date:
    """Parse an API date or return the current local date when it is omitted.

    Raises an HTTP 422 error when the value does not match ``Settings.DATE_FORMAT``.
    """
    if day is None:
        return date.today()

    try:
        return datetime.strptime(day, Settings.DATE_FORMAT).date()
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail="day must be a valid date in DD.MM.YYYY format",
        ) from error


def get_semester_start_day() -> date:
    """Return the configured first study day."""
    try:
        return datetime.strptime(
            Settings.START_DAY,
            Settings.DATE_FORMAT,
        ).date()
    except ValueError as error:
        raise RuntimeError(
            "Settings.START_DAY must be a valid date in DD.MM.YYYY format"
        ) from error


def is_before_semester_start(schedule_date: date) -> bool:
    """Return whether a date is earlier than the first configured study day."""
    return schedule_date < get_semester_start_day()


def get_study_week(schedule_date: date) -> int:
    """Return the academic week number for a date relative to the semester start.

    The Monday-Sunday week containing ``Settings.START_DAY`` is week 1.
    """
    semester_start_day = get_semester_start_day()

    semester_week_start = semester_start_day - timedelta(
        days=semester_start_day.weekday(),
    )
    schedule_week_start = schedule_date - timedelta(days=schedule_date.weekday())
    weeks_from_start = (schedule_week_start - semester_week_start).days // 7
    return weeks_from_start + 1


def is_odd_study_week(schedule_date: date) -> bool:
    """Return whether a date belongs to an odd week in the configured schedule."""
    study_week = get_study_week(schedule_date)

    if (study_week - 1) % 2 == 0:
        return Settings.IS_ODD_START_DAY_WEEK
    return not Settings.IS_ODD_START_DAY_WEEK


def categorize_schedule(
    schedule_response: list[LessonResponse],
    schedule_date: date | None = None,
) -> dict:
    """Split a day's lessons into past, current, and upcoming categories.

    Lessons are compared with the current local date and time. When
    ``schedule_date`` is omitted, the current local date is used.
    """
    now = datetime.now()
    schedule_date = schedule_date or now.date()

    past = []
    current = None
    upcoming = []

    for lesson in schedule_response:
        start_time = datetime.combine(
            schedule_date,
            datetime.strptime(lesson.start_time, "%H:%M").time(),
        )
        end_time = datetime.combine(
            schedule_date,
            datetime.strptime(lesson.end_time, "%H:%M").time(),
        )

        if end_time <= now:
            past.append(lesson)

        elif start_time <= now < end_time:
            current = lesson

        else:
            upcoming.append(lesson)

    return {
        "past": past,
        "current": current,
        "upcoming": upcoming,
    }
