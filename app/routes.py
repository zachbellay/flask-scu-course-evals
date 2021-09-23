from flask import (
    Flask,
    redirect,
    request,
    url_for,
    render_template,
    jsonify,
    send_from_directory,
)
from flask_nav import Nav
from flask_nav.elements import *
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from datetime import datetime
import requests
import json
import os
from distutils.util import strtobool

from . import filters
from app import app
from app import db
from app import whitelist
from app.models import (
    User,
    Eval,
    ClassEval,
    ProfessorEval,
    MajorEval,
    CourseProfessorEval,
)

login_manager = LoginManager()
login_manager.init_app(app)

client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])

# Initializing Navbar
nav = Nav()

# registers the "top" menubar
topbar = Navbar("", View("Home", "index"), View("Logout", "logout"))

nav.register_element("top", topbar)

nav.init_app(app)


@app.route("/haha")
def haha():
    raise Exception("500")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/professor/<professor_name>")
@login_required
def professor(professor_name):

    professor_eval = ProfessorEval.query.filter(
        ProfessorEval.instructor_name == professor_name
    ).all()
    course_professor_eval = CourseProfessorEval.query.filter(
        CourseProfessorEval.instructor_name == professor_name
    ).all()

    if professor_eval is not None:
        return render_template(
            "professor.html",
            professor_name=professor_name,
            professor_eval=professor_eval,
            course_professor_eval=course_professor_eval,
        )
    else:
        return redirect(url_for("index"))


@app.route("/course/<subject>/<subject_number>")
@login_required
def course(subject, subject_number):

    subject = subject.upper()

    class_eval = ClassEval.query.get((subject, subject_number))
    course_professor_eval = (
        CourseProfessorEval.query.filter(CourseProfessorEval.subject == subject)
        .filter(CourseProfessorEval.subject_number == subject_number)
        .all()
    )

    if class_eval is not None:
        return render_template(
            "course.html",
            class_eval=class_eval,
            course_professor_eval=course_professor_eval,
        )
    else:
        return redirect(url_for("index"))


@app.route("/protected/<path:filename>")
@login_required
def protected(filename):
    return send_from_directory(os.path.join(app.root_path, "protected"), filename)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config["GOOGLE_CLIENT_ID"], app.config["GOOGLE_CLIENT_SECRET"]),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        if "scu.edu" not in users_email.split(
            "@"
        ) and "alumni.scu.edu" not in users_email.split("@"):
            return "User email not in scu.edu or alumni.scu.edu.", 400

        if strtobool(app.config["WHITELIST_ENABLED"]):
            if users_email not in whitelist.whitelist:
                return (
                    "User email not in whitelist, people e-mail zbellay@scu.edu to be added to the whitelist",
                    403,
                )

    else:
        return "User email not available or not verified by Google.", 400

    user = User(id=unique_id, name=users_name, email=users_email, active=True)

    # Doesn't exist? Add it to the database.
    if not User.query.filter(User.email == users_email).all():
        db.session.add(user)
        db.session.commit()
    else:
        user = User.query.filter(User.email == users_email).first()

    # Begin user session by logging the user in
    login_user(user)
    print(users_name, users_email)

    # Send user back to homepage
    return redirect(url_for("index"))


def get_google_provider_cfg():
    return requests.get(app.config["GOOGLE_DISCOVERY_URL"]).json()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
