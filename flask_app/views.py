from flask_app.flask_server import app, cache, db
from flask_app import models
from flask import render_template
import time
import cinemas
import multitreading_kinopoisk_fetcher



@app.route('/')
@cache.cached(timeout=5000)
def films_list():
    afisha_raw_html = cinemas.fetch_afisha_page()
    films = cinemas.parse_afisha_list(afisha_raw_html)
    films = sorted(films, key=lambda f: f['count_cinema'], reverse=True)[:10]
    films = multitreading_kinopoisk_fetcher.fetch_raiting_films_in_kinopoisk(films)
    save_fetched_films(films)
    return render_template('films_list.html', films=films)


def save_fetched_films(films):
    for film in films:
        if film['rating'] == '0.0':
            continue
        film_in_database = db.session.query(models.Film)
        film_in_database = film_in_database.filter(models.Film.title == film['title'])
        if film_in_database.count() > 0:
            continue
        new_film = create_film(film)
        db.session.add(new_film)
    db.session.commit()


def create_film(film):
    new_film = models.Film()
    new_film.title = film['title']
    new_film.count_cinema = film['count_cinema']
    new_film.rating = film['rating']
    new_film.image = film['image']
    return new_film
