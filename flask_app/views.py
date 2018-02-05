from flask_app.flask_server import app, cache
from flask import render_template
import time
import cinemas


@app.route('/')
@cache.cached(timeout=5000)
def films_list():
    afisha_raw_html = cinemas.fetch_afisha_page()
    films = cinemas.parse_afisha_list(afisha_raw_html)
    films = sorted(films, key=lambda f: f['count_cinema'], reverse=True)[:10]
    return render_template('films_list.html', films=films)
