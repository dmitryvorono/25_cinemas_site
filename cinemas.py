import requests
from bs4 import BeautifulSoup
import argparse
import sys
import multitreading_kinopoisk_fetcher


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


def output_movies_to_console(movies):
    output_movies = sorted_movies(movies)
    for movie in output_movies:
        print('{0} {1} {2}'.format(movie['title'],
                                   movie['rating'],
                                   movie['image']))


def create_parser():
    parser = argparse.ArgumentParser(description='This script generate rating films showing in Moscow. List cinemas get in afish.ru, rating - kinopoisk.ru')
    parser.add_argument('-c', '--cinema', type=int, help='If input in rating will not include films with count_cinema less than input value')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    afisha_raw_html = fetch_afisha_page()
    films = parse_afisha_list(afisha_raw_html)
    if args.cinema:
        films = filter_movies(films, args.cinema)
    films = multitreading_kinopoisk_fetcher.fetch_raiting_films_in_kinopoisk(films)
    output_movies_to_console(films)
    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
