import os


basedir = os.path.abspath(os.path.dirname(__file__))
site_ip_address = '0.0.0.0'
site_port = 8080
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.environ['FLASK_DB_FILENAME'])
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
TIME_OUT_CACHE = 5000
COUNT_FILMS_ON_PAGE = 12
