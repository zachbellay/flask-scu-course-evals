from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_sslify import SSLify
from .whitelist import Whitelist
from flask_compress import Compress

dotenv_path = os.path.join(os.path.dirname(__file__), '../' , '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config.from_object(os.environ['APP_CONFIG'])
whitelist_path = os.path.join(os.path.dirname(__file__), '../' , 'WHITELIST.txt')
whitelist = Whitelist(app, whitelist_path)
Compress(app)
sslify = SSLify(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models