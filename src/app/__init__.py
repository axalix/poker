from flask import Flask
from flask_sqlalchemy import SQLAlchemy

poker = Flask(__name__)
poker.config.from_object('config')
db = SQLAlchemy(poker)

from app import views, models
