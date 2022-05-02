from warnings import warn

ESPECES_PAR_PAGE = 10
SECRET_KEY = "pain_de_vie"
API_ROUTE = "/api" #TODO


if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)


class _TEST:
    SECRET_KEY = SECRET_KEY
    # On configure la base de données
    SQLALCHEMY_DATABASE_URI = 'sqlite:///BioDiVienne.db'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BioDivVie2.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'biodivienne/static/uploads/'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

class _PRODUCTION:
    SECRET_KEY = SECRET_KEY
    # On configure la base de données
    #SQLALCHEMY_DATABASE_URI = 'mysql://gazetteer_user:password@localhost/gazetteer'
    #SQLALCHEMY_DATABASE_URI = 'mysql:///BioDiVienne_prod.db' # hypothèse production sur mysql
    SQLALCHEMY_DATABASE_URI = 'sqlite:///BioDiVienne.db' #TEST
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'biodivienne/static/uploads/'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

CONFIG = {
    "test": _TEST,
    "production": _PRODUCTION
}

#gestion des images
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

