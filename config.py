import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))
SITE_IP_ADDRESS = '0.0.0.0'
SITE_PORT = 8080
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR , os.environ['FLASK_DB_FILENAME'])
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR , 'db_repository')
TIME_OUT_CACHE = 5000
COUNT_FILMS_ON_PAGE = 12
COUNT_FETCHERS = 4
