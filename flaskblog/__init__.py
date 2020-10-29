#This is the file where we intialize and configure everything
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from flaskblog.config import Config


db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login'
#info is just a simple bootstrap category for styling the text
login_manager.login_message_category='info'

#Please use environment variables here
mail=Mail()



def create_app(config_class=Config):
	app=Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	with app.app_context():
		db.create_all()
	bcrypt.init_app(app)
	login_manager.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main
	from flaskblog.errors.handlers import errors
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app



