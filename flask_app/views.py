from flask_app.flask_server import app, cache
from flask import render_template
import cinemas
from config import TIME_OUT_CACHE


@app.route('/')
@cache.cached(timeout=TIME_OUT_CACHE)
def films_list():
    films = cinemas.get_film_for_render()
    return render_template('films_list.html',
                           films=films)
