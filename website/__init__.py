# it makes the website folder a python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# creating a database
db = SQLAlchemy()
DB_NAME = "database.db"

def  create_app():
	app = Flask(__name__)
	 # it secures the cookies and session data from the website.
	app.config['SECRET_KEY'] = '9902888858'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	# sqlite:///{DB_NAME} is the location where the db is stored.
	# initialize our db
	db.init_app(app) 

	# blueprints are imported
	# relative imports
	from .view import views
	from .auth import auth
	#register blueprints with flask
	app.register_blueprint(views,url_prefix='/')
	app.register_blueprint(auth,url_prefix='/')

	# we import the models.py file so that the classes in it are initialized properly before running the app.
	from .models import User,Note

	# create_database(app) -> not working
	# There is no need for that create_database function. SQLAlchemy will already not overwrite an existing file, and the only time the database wouldn't be created is if it raised an error.
	# Flask-SQLAlchemy 3 no longer accepts an app argument to methods like create_all. Instead, it always requires an active Flask application context.
	with app.app_context():
		db.create_all()

	login_manager = LoginManager()
	login_manager.login_view = "auth.login"
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app

def create_database(app):
	if not path.exists('website/'+ DB_NAME):
		db.create_all(app=app)
		print('Database created')

