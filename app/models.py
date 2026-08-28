from sqlalchemy import Boolean, Column, Integer, Text

from app.db import Base


# Schedule models
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, index=True)


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    teacher_name = Column(Text, nullable=True)

    # Inclusive study-week range. None means that the boundary is not limited.
    start_week = Column(Integer, nullable=True)
    end_week = Column(Integer, nullable=True)


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    location_short = Column(Text, nullable=True)
    location = Column(Text, nullable=False)

    # True — odd week, False — even week, None — every week.
    is_odd_week = Column(Boolean, nullable=True)

    # Relationships
    subject_id = Column(Integer, nullable=False)
    group_id = Column(Integer, nullable=False)


# Score models
class SubjectScore(Base):
    __tablename__ = "subject_scores"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
    subject_id = Column(Integer, nullable=False)
    telegram_user_id = Column(Integer, nullable=False, unique=True)
