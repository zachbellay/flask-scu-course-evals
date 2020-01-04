### Setup
- To get database up and running run
    - `flask db migrate && flask db upgrade`
- To populate evaluations into database run `python3 csv_to_sqlite.py`
- To run development server run `flask run --cert=cert.pem --key=key.pem`

Docker Dev Server:
`docker run -p 443:5000 registry.gitlab.com/zachbellay/flask-scu-course-evals:latest`