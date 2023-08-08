# used to store database models
from . import db
# we are importing dbfrom the current package -> website
# . -> package

from flask_login import UserMixin
from sqlalchemy.sql import func
# ----------------------.#
# tables model in database
class Note(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	data = db.Column(db.String(1000))
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key = True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(100))
	notes = db.relationship('Note')