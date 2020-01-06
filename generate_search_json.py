import os
import numpy as np
import json

from app.models import Eval, ClassEval, ProfessorEval

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_CONFIG'])
db = SQLAlchemy(app)

def get_course_with_names():
    courses_with_names = []

    # Get all class evals
    class_evals = ClassEval.query.all()

    for row in class_evals:
        course_with_name = row.subject + ' ' + row.subject_number + ' ' + row.class_name
        courses_with_names.append({'name' : course_with_name})
    
    return courses_with_names

def get_professors():
    professors = []

    # Get all professor names
    professor_evals = ProfessorEval.query.all()

    for row in professor_evals:
        professors.append({'name' : row.instructor_name})

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