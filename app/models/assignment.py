from sqlmodel import SQLModel, Field, Relationship
import os
from typing import Optional
from datetime import date

class Assignment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    due_date: Optional[date]
    course_id: Optional[int] = Field(default=None, foreign_key="course.id")
    course: Optional["Course"] = Relationship(back_populates="assignments")
