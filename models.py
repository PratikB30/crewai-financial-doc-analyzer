from sqlalchemy import Column, Integer, String, Text
from database import Base

class TaskResult(Base):
    __tablename__ = "task_results"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    status = Column(String, default="PENDING")
    file_path = Column(String)
    result = Column(Text, nullable=True)
