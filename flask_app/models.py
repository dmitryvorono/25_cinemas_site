from flask_app.flask_server import db


class Film(db.Model):
    __tablename__ = 'films'
    identifier = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String)
    count_cinema = db.Column(db.Integer)
    rating = db.Column(db.Float)
    image = db.Column(db.String)
