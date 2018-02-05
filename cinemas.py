import requests
from bs4 import BeautifulSoup
import argparse
import random
import itertools
import os
import json
import sys


def load_fake_headers(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def load_proxies_list(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as proxies_file:
        return proxies_file.read().split()


def fetch_afisha_page():
    request = requests.get('https://www.afisha.ru/msk/schedule_cinema/')
    if request.status_code == requests.codes.ok:
        return request.content


def parse_afisha_list(raw_html):
    afisha_html_tree = BeautifulSoup(raw_html, 'html.parser')
    film_elements = afisha_html_tree.find_all('div', {'class': 'object s-votes-hover-area collapsed'})
    return [{'title': f.find('h3').text, 'count_cinema': len(f.find_all('tr'))} for f in film_elements]


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


def is_bad_html(raw_html):
    if raw_html is None:
        return True
    movie_info_tree = BeautifulSoup(raw_html, 'html.parser')
    capcha = movie_info_tree.find('img', {'class': 'image form__captcha'})
    return bool(capcha)


def fetch_movie_info(movie_title, cycle_proxy, fake_headers):
    url = 'https://www.kinopoisk.ru/index.php?first=yes&what=&kp_query={0}'.format(movie_title)
    movie_info = None
    while movie_info is None:
        proxies = {'https': next(cycle_proxy)}
        headers = next(fake_headers)
        movie_info = try_fetch_by_proxy(url, proxies, headers)
        if is_bad_html(movie_info):
            movie_info = None
    return movie_info


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


def filter_movies(movies, count_cinemas):
    return list(filter(lambda f: f['count_cinema'] >= count_cinemas, movies))


def sorted_movies(movies):
    return sorted(movies, key=lambda f: float(f['rating']) if f['rating'] is not None else 0, reverse=True)


def output_movies_to_console(movies):
    output_movies = sorted_movies(movies)
    for m in output_movies:
        print('{0} {1}'.format(m['title'], m['rating']))


def create_parser():
    parser = argparse.ArgumentParser(description='This script generate rating films showing in Moscow. List cinemas get in afish.ru, rating - kinopoisk.ru')
    parser.add_argument('-c', '--cinema', type=int, help='If input in rating will not include films with count_cinema less than input value')
    return parser


def get_cycle_proxies(filepath):
    proxies_list = load_proxies_list(filepath)
    random.shuffle(proxies_list)
    return itertools.cycle(set(proxies_list))


def main():
    parser = create_parser()
    args = parser.parse_args()
    afisha_raw_html = fetch_afisha_page()
    films = parse_afisha_list(afisha_raw_html)
    cycle_proxy = get_cycle_proxies('proxies.txt')
    fake_headers = itertools.cycle(load_fake_headers('fake_headers.txt'))
    if args.cinema:
        films = filter_movies(films, args.cinema)
    for f in films:
        print('Fetch: {0}'.format(f['title']))
        movie_info = fetch_movie_info(f['title'], cycle_proxy, fake_headers)
        f.update(parse_movie_info(movie_info))
    output_movies_to_console(films)
    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
