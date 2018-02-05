from flask import Flask
from flask.ext.cache import Cache
app = Flask(__name__)
app.config.from_object('config')
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
from flask_app import views
