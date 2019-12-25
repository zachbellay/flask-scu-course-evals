from app import db
from flask_security import UserMixin
from sqlalchemy import Column, INTEGER, VARCHAR, Boolean, FLOAT, CHAR

class User(db.Model, UserMixin):
  __tablename__ = "users"

  id = Column(VARCHAR(), primary_key=True)
  email = Column(VARCHAR(), unique=True)
  active = Column(Boolean)
  name = Column(VARCHAR())

class Evals(db.Model):
    id = Column(INTEGER(), primary_key=True)
    year = Column(INTEGER())
    quarter = Column(CHAR(6))
    course_id = Column(INTEGER())
    instructor_name = Column(VARCHAR())
    subject = Column(CHAR(4))
    subject_number = Column(CHAR(5))
    response_rate = Column(FLOAT())
    num_enrolled = Column(INTEGER())
    num_responses = Column(INTEGER())
    class_name=Column(VARCHAR())
    overall_avg=Column(FLOAT())
    overall_std_dev=Column(FLOAT())
    difficulty_avg=Column(FLOAT())
    difficulty_med=Column(FLOAT())
    difficulty_std_dev=Column(FLOAT())
    avg_weekly_workload=Column(FLOAT())
    