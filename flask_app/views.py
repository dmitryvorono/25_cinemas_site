from flask_app.flask_server import app, cache
from flask import render_template
import time


@app.route('/')
@cache.cached(timeout=50)
def films_list():
    time.sleep(15)
    return render_template('films_list.html')
