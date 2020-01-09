import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import * 
import os
import numpy as np

from app.models import Eval, ClassEval, ProfessorEval, MajorEval, CourseProfessorEval

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, Column
from sqlalchemy.types import * 

app = Flask(__name__)
app.config.from_object(os.environ['APP_CONFIG'])
db = SQLAlchemy(app)

def get_latest_name(evals, subject, subject_number):
    matches = []
    for eval_ in evals.itertuples():
        if(eval_.subject == subject and eval_.subject_number == subject_number):
            matches.append(eval_)
    
    matches = pd.DataFrame(matches)

    quarters = { 'Winter' : 0, 'Spring' : 1, 'Summer' : 2, 'Fall' : 3 }

    matches['quarter_sort'] = matches['quarter'].replace(quarters)

    matches.sort_values(by=['quarter_sort'], inplace=True, ascending=False)
    matches.sort_values(by=['year'], inplace=True, ascending=False)
    
    latest_match = matches.iloc[0]

    return latest_match.class_name


def create_evals_table(evals):
  # Calculate avg weekly workload       
  evals['avg_weekly_workload'] = (0.5  * (evals['zero_one']/100))  + \
                                (2.5  * (evals['two_three']/100)) + \
                                (4.5  * (evals['four_five']/100)) + \
                                (6.5  * (evals['six_seven']/100)) + \
                                (9.0  * (evals['eight_ten']/100)) + \
                                (12.5 * (evals['eleven_fourteen']/100)) + \
                                (15.0 * (evals['fifteen_plus']/100))

  # # Remove individual hourly columns (saves space)
  evals = evals.drop(columns=['zero_one', 'two_three', 'four_five', 'six_seven', 'eight_ten', 'eleven_fourteen', 'fifteen_plus'])

  evals = evals.round(3)

  for row in evals.itertuples():
    eval_ = Eval(id=row.Index,
                 year=row.year,
                 quarter=row.quarter,
                 course_id=row.course_id,
                 instructor_name=row.instructor_name,
                 subject=row.subject,
                 subject_number=row.subject_number,
                 num_enrolled=row.num_enrolled,
                 num_responses=row.num_responses,
                 class_name=row.class_name,
                 overall_avg=row.overall_avg,
                 overall_std_dev=row.overall_std_dev,
                 difficulty_avg=row.difficulty_avg,
                 difficulty_std_dev=row.difficulty_std_dev,
                 avg_weekly_workload=row.avg_weekly_workload)
    db.session.add(eval_)
  db.session.commit()

  return evals

def create_class_evals_table(evals):
  class_evals = pd.pivot_table(evals, 
                              index=['subject', 'subject_number'],
                              aggfunc={'overall_avg' : np.mean,
                                        'difficulty_avg' : np.mean,
                                        'avg_weekly_workload' : np.mean                             
                                      }
                              )
  class_evals['class_name']=''
  class_evals.reset_index(inplace=True)
  class_evals.set_index(['subject', 'subject_number'], inplace=True)
  class_evals.sort_index(inplace=True)

  for subject, subject_number in class_evals.index:
      class_name = get_latest_name(evals, subject, subject_number)
      class_evals['class_name'].loc[subject, subject_number] = class_name
  
  for row in class_evals.itertuples():
    class_eval = ClassEval(subject=row.Index[0],
                           subject_number=row.Index[1],
                           class_name=row.class_name,
                           overall_avg=row.overall_avg,
                           difficulty_avg=row.difficulty_avg,
                           avg_weekly_workload=row.avg_weekly_workload)
    db.session.add(class_eval)
  db.session.commit()

def create_professor_evals_table(evals):
  professor_evals = pd.pivot_table(evals,
                                  index=['instructor_name'],
                                  aggfunc={'overall_avg' : np.mean,
                                           'difficulty_avg' : np.mean,
                                           'avg_weekly_workload' : np.mean                                  
                                          }
                                  )
  for row in professor_evals.itertuples():
    professor_eval = ProfessorEval(instructor_name=row.Index,
                                   overall_avg=row.overall_avg,
                                   difficulty_avg=row.difficulty_avg,
                                   avg_weekly_workload=row.avg_weekly_workload)
    db.session.add(professor_eval)
  db.session.commit()

def create_major_evals_table(evals):
  major_evals = pd.pivot_table(evals,
                               index=['subject'],
                               aggfunc={'overall_avg' : np.mean,
                                        'difficulty_avg' : np.mean,
                                        'avg_weekly_workload' : np.mean                                  
                                      }
                              )
  for row in major_evals.itertuples():
    major_eval = MajorEval(subject=row.Index,
                           overall_avg=row.overall_avg,
                           difficulty_avg=row.difficulty_avg,
                           avg_weekly_workload=row.avg_weekly_workload)
    db.session.add(major_eval)
  db.session.commit()


def create_course_professor_table(evals):
  course_professor_evals = pd.pivot_table(evals,
                                         index=['subject', 'subject_number', 'class_name', 'instructor_name'],
                                         aggfunc={'overall_avg' : np.mean,
                                                  'difficulty_avg' : np.mean,
                                                  'avg_weekly_workload' : np.mean                                  
                                                 }
                                         )
  for row in course_professor_evals.itertuples():
    course_professor_eval = CourseProfessorEval(
                            subject=row.Index[0],
                            subject_number=row.Index[1],
                            class_name=row.Index[2],
                            instructor_name=row.Index[3],
                            overall_avg=row.overall_avg,
                            difficulty_avg=row.difficulty_avg,
                            avg_weekly_workload=row.avg_weekly_workload)
    db.session.add(course_professor_eval)
  db.session.commit()                                      

def main():
  
  evals = pd.read_csv('course_evals.csv')

  evals_table_df = create_evals_table(evals)
  create_class_evals_table(evals_table_df)
  create_professor_evals_table(evals_table_df)
  create_major_evals_table(evals_table_df)
  create_course_professor_table(evals)

if __name__ == '__main__':
  main()