import json
import os

import numpy as np
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.models import ClassEval, Eval, ProfessorEval

app = Flask(__name__)
app.config.from_object(os.environ['APP_CONFIG'])
db = SQLAlchemy(app)

def get_course_with_names():
    courses_with_names = []

    # Get all class evals
    class_evals = ClassEval.query.all()

    for row in class_evals:
        try:
            course_with_name = row.subject + ' ' + row.subject_number + ' ' + row.class_name
            courses_with_names.append({'name' : course_with_name})
        except:
            print('Subject: ' + row.subject if row.subject else 'None')
            print('Subject Number: ' + row.subject_number if row.subject_number else 'None')
            print('Class Name: ' + row.class_name if row.class_name else 'None')
    
    return courses_with_names

def get_professors():
    professors = []

    professor_set = set()

    # Get all professor names
    professor_evals = ProfessorEval.query.all()

    for row in professor_evals:
        if(row.instructor_name not in professor_set):
            professors.append({'name' : row.instructor_name})
            professor_set.add(row.instructor_name)

    return professors

def main():

    courses_with_names = get_course_with_names()
    professors = get_professors()

    search_suggestion_json = {
                                'courses' : courses_with_names,
                                'professors' : professors
                             }

    with open('app/protected/courses_with_names.json', 'w') as f:
        json.dump(search_suggestion_json, f)


if __name__ == '__main__':
    main()
