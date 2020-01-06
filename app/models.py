from app import db
from datetime import datetime
from flask_security import UserMixin
from sqlalchemy import create_engine, Column
from sqlalchemy.types import * 

class User(db.Model, UserMixin):
  __tablename__ = "users"

  id = Column(VARCHAR(), primary_key=True)
  email = Column(VARCHAR(), unique=True)
  active = Column(Boolean)
  name = Column(VARCHAR())
  last_seen = Column(db.DateTime, default=datetime.utcnow)

class Eval(db.Model):
  __tablename__ = "evals"

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

class ClassEval(db.Model):
  __tablename__ = "class_evals"

  subject = Column(CHAR(4), primary_key=True)
  subject_number = Column(CHAR(5), primary_key=True)
  class_name=Column(VARCHAR())
  overall_avg=Column(FLOAT())
  difficulty_avg=Column(FLOAT())
  avg_weekly_workload=Column(FLOAT())

class ProfessorEval(db.Model):
  __tablename__ = "professor_evals"

  instructor_name = Column(VARCHAR(), primary_key=True)
  overall_avg=Column(FLOAT())
  difficulty_avg=Column(FLOAT())
  avg_weekly_workload=Column(FLOAT())

class MajorEval(db.Model):
  __tablename__ = "major_evals"

  subject = Column(CHAR(4), primary_key=True)
  overall_avg=Column(FLOAT())
  difficulty_avg=Column(FLOAT())
  avg_weekly_workload=Column(FLOAT())