from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
from flask import flash, redirect, url_for

from flask_login import LoginManager, current_user, logout_user, login_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# concernant la sauvegarde des images : Crédits Roy's tutorial : https://roytuts.com/upload-and-display-image-using-python-flask/
from .constantes import CONFIG, ALLOWED_EXTENSIONS




def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

# On initie l'extension
db = SQLAlchemy()
login = LoginManager()

#INITIALISATION DES VARIABLES
app = Flask(
    __name__,
    template_folder=templates,
    static_folder=statics
)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BioDiVienne.db'  #TEST
from .routes import generic

def config_app(config_name="test"):
    """ Create the application """
    app.config.from_object(CONFIG[config_name])
    # Set up extensions
    db.init_app(app)
    # assets_env = Environment(app)
    login.init_app(app)

    # Register Jinja template functions

    return app

# On crée nos différents modèles



if __name__ == "__main__":
    app.run(debug=True)

