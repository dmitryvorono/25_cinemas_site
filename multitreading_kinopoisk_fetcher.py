import queue
import threading
import os
import random
import itertools
import json
import requests
from bs4 import BeautifulSoup
count_fetchers = 5


def try_fetch_by_proxy(url, proxy, headers):
    session = requests.session()
    session.headers.update(headers)
    session.proxies.update(proxy)
    try:
        request = session.get(url, timeout=10)
    except:
        return None
    if request.status_code == requests.codes.ok:
        return request.text


def is_captcha_html(raw_html):
    if raw_html is None:
        return True
    movie_info_tree = BeautifulSoup(raw_html, 'html.parser')
    capcha = movie_info_tree.find('img', {'class': 'image form__captcha'})
    return bool(capcha)


def get_html_text(html_tree, tag, attrs):
    target_element = html_tree.find(tag, attrs)
    if target_element is not None:
        return target_element.text


def parse_movie_info(raw_html):
    if raw_html is None:
        return {'rating': '0.0', 'count_votes': '0.0'}
    movie_info_tree = BeautifulSoup(raw_html, 'html.parser')
    rating = get_html_text(movie_info_tree, 'span', {'class': 'rating_ball'})
    count_votes = get_html_text(movie_info_tree, 'span', {'class': 'ratingCount'})
    return {'rating': rating, 'count_votes': count_votes}


def start_fetcher(film, proxy, headers):
    url = 'https://www.kinopoisk.ru/index.php?first=yes&what=&kp_query={0}'.format(film['title'])
    raw_kinopoisk_html = try_fetch_by_proxy(url, proxy, headers)
    if is_captcha_html(raw_kinopoisk_html):
        return film
    film.update(parse_movie_info(raw_kinopoisk_html))


def start_worker(queue_unprocessed_films, proxy, headers):
    while True:
        film = queue_unprocessed_films.get()
        if film is None:
            break
        start_fetcher(film, proxy, headers)
        queue_unprocessed_films.task_done()


def load_proxies_list(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as proxies_file:
        return proxies_file.read().split()


def get_cycle_proxies(filepath):
    proxies_list = load_proxies_list(filepath)
    random.shuffle(proxies_list)
    return itertools.cycle(set(proxies_list))


def load_fake_headers(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def fetch_raiting_films_in_kinopoisk(films):
    queue_unprocessed_films = queue.Queue()
    cycle_proxy = get_cycle_proxies('proxies.txt')
    cycle_fake_headers = itertools.cycle(load_fake_headers('fake_headers.txt'))
    film_fetchers = [threading.Thread(target=start_worker,
                                      args=(queue_unprocessed_films,
                                            {'https': next(cycle_proxy)},
                                            next(cycle_fake_headers)))
                     for i in range(count_fetchers)]
    for film_fetcher in film_fetchers:
        film_fetcher.start()
    for item in films:
        queue_unprocessed_films.put(item)
    queue_unprocessed_films.join()
    for i in range(count_fetchers):
        queue_unprocessed_films.put(None)
    for film_fetcher in film_fetchers:
        film_fetcher.join()
    return films
