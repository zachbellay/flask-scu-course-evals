import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    DEBUG = False
    TESTING = False
    WHITELIST_ENABLED = os.environ.get("WHITELIST_ENABLED", False)
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Google Login Information
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    OAUTH_REDIRECT_SCHEME = os.environ.get("OAUTH_REDIRECT_SCHEME", "https")

class ProductionConfig(Config):   
    GOOGLE_CLIENT_ID = os.environ.get("PROD_GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("PROD_GOOGLE_CLIENT_SECRET", None)

class DevelopmentConfig(Config):
    GOOGLE_CLIENT_ID = os.environ.get("DEV_GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("DEV_GOOGLE_CLIENT_SECRET", None)
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
