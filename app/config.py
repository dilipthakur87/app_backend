import os

from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', os.getenv("DATABASE_URL", "notes.db"))}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_RUN_PORT =  os.getenv('FLASK_RUN_PORT', 5500)

    # Celery Configuration
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://redis:6379/0')

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
