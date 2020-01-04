from app import app as application

if __name__ == "__main__":
    application.run(host='0.0.0.0')

# gunicorn --bind 0.0.0.0:5000 wsgi
# gunicorn --bind 0.0.0.0:443 --certfile cert.pem --keyfile key.pem wsgi