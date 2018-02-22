from flask_app.flask_server import app, cache, db
from flask_app.models import Film
from flask import render_template
import cinemas
from multitreading_kinopoisk_fetcher import fetch_raiting_films_in_kinopoisk
from config import TIME_OUT_CACHE, COUNT_FILMS_ON_PAGE


@app.route('/')
@cache.cached(timeout=TIME_OUT_CACHE)
def films_list():
    afisha_raw_html = cinemas.fetch_afisha_page()
    films = cinemas.parse_afisha_list(afisha_raw_html)
    films = sorted(films, key=lambda film: film['count_cinema'], reverse=True)
    films = films[:COUNT_FILMS_ON_PAGE]
    fetched_films = []
    films_need_kinopoins_fetch = []
    delete_film_without_rating()
    for film in films:
        saved_film = get_saved_film(film)
        if saved_film:
            fetched_films.append(saved_film)
        else:
            films_need_kinopoins_fetch.append(film)
    films_need_kinopoins_fetch = fetch_raiting_films_in_kinopoisk(films_need_kinopoins_fetch)
    saved_films = save_fetched_films(films_need_kinopoins_fetch)
    return render_template('films_list.html',
                           films=fetched_films + saved_films)


def get_saved_film(film):
    film_in_database = db.session.query(Film)
    film_in_database = film_in_database.filter(Film.title == film['title'])
    if film_in_database.count() == 0:
        return None
    return film_in_database.first()


def save_fetched_films(films):
    saved_films = []
    for film in films:
        if film['rating'] == '0.0':
            continue
        new_film = create_film(film)
        db.session.add(new_film)
        saved_films.append(new_film)
    db.session.commit()
    return saved_films


def delete_film_without_rating():
    query_films = db.session.query(Film).filter(Film.rating == None)
    if query_films.count() == 0:
        return 0
    count_deleted_films = query_films.delete(synchronize_session=False)
    db.session.commit()
    return count_deleted_films


def create_film(film):
    new_film = Film()
    new_film.title = film['title']
    new_film.count_cinema = film['count_cinema']
    new_film.rating = film['rating']
    new_film.image = film['image']
    return new_film
