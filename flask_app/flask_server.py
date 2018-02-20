from flask import Flask
from flask.ext.cache import Cache
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
from flask_app import views, models
