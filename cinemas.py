import requests
from bs4 import BeautifulSoup
from multitreading_kinopoisk_fetcher import fetch_raiting_films_in_kinopoisk
from flask_app.flask_server import db
from flask_app.models import Film
from config import COUNT_FILMS_ON_PAGE


def fetch_afisha_page():
    request = requests.get('https://www.afisha.ru/msk/schedule_cinema/')
    if request.status_code == requests.codes.ok:
        return request.content


def parse_afisha_list(raw_html):
    afisha_html_tree = BeautifulSoup(raw_html, 'html.parser')
    film_elements = afisha_html_tree.find_all('div', {'class': 'object s-votes-hover-area collapsed'})
    return [{'title': film_element.find('h3').text,
            'count_cinema': len(film_element.find_all('tr'))}
            for film_element in film_elements]


def filter_movies(movies, count_cinemas):
    return list(filter(lambda f: f['count_cinema'] >= count_cinemas, movies))


def sorted_movies(movies):
    return sorted(movies,
                  key=lambda film: float(film['rating']) if film['rating'] is not None else 0,
                  reverse=True)


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
    query_films = db.session.query(Film).filter(Film.rating.is_(None))
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


def get_film_for_render():
    afisha_raw_html = fetch_afisha_page()
    films = parse_afisha_list(afisha_raw_html)
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
    return fetched_films + saved_films
