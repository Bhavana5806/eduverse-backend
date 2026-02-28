from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class StudentPerformance(Base):
    __tablename__ = "student_performance"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    subject = Column(String)
    topic = Column(String)
    score = Column(Float)
    max_score = Column(Float)