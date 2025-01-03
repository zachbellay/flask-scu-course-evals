### Environment Setup:

Do this on an intel x86 machine, as opposed to an M1 Mac, see note

Why: You need to do this so that packages can be installed appropriately and not conflict with your system's python. There is a good chance that by using your system python this won't work.

My recommended approach for python virtual environments is to use pyenv. You can use whatever approach you prefer, but this is what I'd suggest:

Step 1: Install pyenv
- `curl https://pyenv.run | bash`

Step 2: Add pyenv commands to your bashrc (or other shell config):
- Follow instructions for your specific shell here: https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv

Step 3: Install Python 3.7
- `pyenv install 3.7`

Step 4: Create `scu-course-evals` environment
- `pyenv virtualenv 3.7 scu-course-evals`

Step 5: Set `scu-course-evals` as local environment (specific to this directory)
- `pyenv local scu-course-evals`

Step 5b (Optional): If that doesn't work run `pyenv shell scu-course-evals`

Step 6: Install dependencies:
- `pip install -r requirements.txt && pip install pandas scipy`

_Note: As far as I know, scipy doesn't work on M1 Macs (at least I haven't been able to get it to work) so I would suggest using x86 architecture intel machines_ 


### Database Setup
- If the database doesn't exist yet (i.e. `db/app.db` doesn't exist yet) run 
    - `flask db stamp head`
- To populate the database's schema run:
    - `flask db migrate && flask db upgrade`
- To populate evaluations into database run: 
    - `python3 csv_to_sqlite.py`


- To run development server run: 
    - `gunicorn --bind 127.0.0.1:5000 --certfile ./dev-pems/cert.pem --keyfile ./dev-pems/key.pem wsgi`

## Building the docker image

_Note_: The tags are different in the docs, so don't just copy paste. Make sure you are using the proper tags when building and deploying.

- Login to gitlab container registry
    - `docker login registry.gitlab.com`

- To build the image and push to gitlab on an M1 Mac:
    - `docker buildx build --platform linux/amd64 --push -t registry.gitlab.com/zachbellay/flask-scu-course-evals:spring-2021-update .`

Tags:
- spring-2021-update
- june-2023-update

### Prod Setup
- Transfer `app.db` file to server under `~/db`
- To get image: 
    - `docker pull registry.gitlab.com/zachbellay/flask-scu-course-evals:latest`
- To build image:
    `docker buildx build --platform linux/amd64 --push -t registry.gitlab.com/zachbellay/flask-scu-course-evals:july-2023-update .`
- To run image: 
    - `docker run -p 443:5000 -p 80:5000 -v /home/zbellay/db:/src/db registry.gitlab.com/zachbellay/flask-scu-course-evals:latest`

### To Update Database 
1. If you cleared db/app.db, then be sure to run `flask db migrate && flask db upgrade`. Then run `sqlite3 db/app.db` and run the `.tables` command and ensure it returns names of the table.
2. Then run `csv_to_sqlite.py`.


#### TODO
# List of features to add
- [x] Make auto complete suggestions scrollable
- [] Make it so that courses.css is named appropriately or changed or generalized because it is also being used by the professor view.
- ~~[x] Add the relative difference from the average for each metric (20% easier than a typical COEN class, 10% higher quality, etc)~~
- [x] Add percentiles to compare classes/professor w.r.t. each major
- [x] Add major specific teaching for professors (if a professor teaches two majors, it may be good to differentiate things)
- [] Add major specific lists for best professor
- [] Add major specific lists for best classes

