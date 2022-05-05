import os
from flask import Flask
from app.models import db

app = Flask(__name__)

db_uri = os.environ["DATABASE_URL"]
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

db.init_app(app)
db.drop_all()
