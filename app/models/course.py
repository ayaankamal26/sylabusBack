from sqlmodel import SQLModel, Field, Relationship
import os
from typing import List, Optional

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    assignments: List["Assignment"] = Relationship(back_populates="course")
