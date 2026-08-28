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



class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer, nullable=False)
    teacher_name = Column(Text, nullable=True)

    # Inclusive study-week range. None means that the boundary is not limited.
    start_week = Column(Integer, nullable=True)
    end_week = Column(Integer, nullable=True)

    # Time data
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)

    # Location data
    location_short = Column(Text, nullable=True)
    location = Column(Text, nullable=False)

    # True — odd week, False — even week, None — every week.
    is_odd_week = Column(Boolean, nullable=True)

    # Relationships
    subject_id = Column(Integer, nullable=False)
    group_id = Column(Integer, nullable=False)