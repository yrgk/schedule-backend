from pydantic import BaseModel


class LessonResponse(BaseModel):
    title: str
    start_time: str
    end_time: str
    teacher_name: str | None
    location_short: str | None
    location: str
