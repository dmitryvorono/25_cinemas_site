# Cinemas Site

The project is written for show actual fims.

This project is created for educational purposes only. All information about the films are taken from the sites
 [afisha.ru](https://www.afisha.ru/)
and [kinopoisk.ru](https://www.kinopoisk.ru/).

[Open app](https://peaceful-fortress-17177.herokuapp.com/)

# How to run project on local

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
$ pip install -r requirements.txt # alternatively try pip3
```
Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

Next, you must set varialbe `FLASK_DB_FILENAME`:

```bash
$ export FLASK_DB_FILENAME=films.db
```

Next, run app:

```bash
$ python server.py
```

App will open `http://0.0.0.0:8080`

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
