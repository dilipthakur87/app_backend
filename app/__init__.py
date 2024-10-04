from celery import Celery
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
celery =  Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['app.tasks']

    )
celery.conf.update(app.config)
# celery.conf.update(broker_connection_retry_on_startup=True)

mail = Mail()
mail.init_app(app)