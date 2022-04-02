from flask_login import LoginManager
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# Crédits Roy's tutorial : https://roytuts.com/upload-and-display-image-using-python-flask/
import os
#from app import app
import urllib.request
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ESPECES_PAR_PAGE = 5

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#INITIALISATION DES VARIABLES
app = Flask("BioDieVienne")
#On configure la base données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BioDivVie2.db'
# On initie l'extension
db = SQLAlchemy(app)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'foo@bar.tld': {'password': 'secret'}}
class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

#login = LoginManager(app)
#import flask_login
#login_manager.init_app(app)

# On crée nos différents modèles
class Personne(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text)
    prenom = db.Column(db.Text)
    utilisateurON = db.Column(db.Integer)

class User(db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_nom = db.Column(db.Text, nullable=False)
    user_login = db.Column(db.String(45), nullable=False, unique=True)
    user_email = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)

class Compte(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    mail = db.Column(db.Text, unique=True, nullable=False)
    pseudo = db.Column(db.Text, unique=True, nullable=False)
    mdp = db.Column(db.Text, nullable=False)
    photos = db.relationship("Photo", back_populates="compte")

class Photo(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    titre = db.Column(db.Text)
    datePrise = db.Column(db.Text)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    compte = db.relationship("Compte", back_populates="photos")
    lien_interne = db.Column(db.Text, unique=True, nullable=False)
    lien_externe = db.Column(db.Text)

class Espece(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    fichier = db.Column(db.Text, unique=True, nullable=False)
    regne = db.Column(db.Text, nullable=False)
    nom_vernaculaire = db.Column(db.Text)
    nom_latin = db.Column(db.Text)
    description = db.Column(db.Text)
    preoccupation = db.Column(db.Text)
    droit_image = db.Column(db.Text)


@app.route("/espece/<int:id>")
def espece(id):
    unique_espece = Espece.query.get(id)
    return render_template("espece.html", espece=unique_espece)


@app.route("/")
def accueil_(exemple=None):
    especes = Espece.query.all()
    return render_template("accueil4.html", especes=especes)


@app.route("/accueil")
#fonction de lancement de la page d'accueil
def accueil(exemple=None):
    especes = Espece.query.all()
    return render_template("accueil4.html", especes=especes)


@app.route("/recherche")
def recherche():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats = []

    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Espece.query.filter(
            Espece.fichier.like("%{}%".format(motclef))
        ).paginate(page=page, per_page=ESPECES_PAR_PAGE)
        titre = "Résultat pour la recherche `" + motclef + "`"

    return render_template(
        "chercher2.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )



@app.route("/charger")
#fonction pour enregistrer une espèce
def upload_form():
    return render_template("charger19.html")


@app.route("/upload", methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("L'image a été correctement téléchargée.")

        return render_template('charger19.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route("/enregistrer", methods=['POST'])
def enregistrer_image():
    data = request.form #c'est un tableau associatif (clé-valeur) appelé collection en python, ou dictionnaire de données
    filename_data = data["fichier"]
    regne_data = data["regne"]
    vernaculaire_data = data["vernaculaire"]
    latin_data = data["latin"]
    description_data = data["description"]
    preoccupation_data = data["preoccupation"]
    droit_image_data = data["droit_image"]


    espece = Espece(
        fichier=filename_data,
        nom_vernaculaire=vernaculaire_data,
        nom_latin=latin_data,
        description=description_data,
        regne=regne_data,
        preoccupation=preoccupation_data,
        droit_image=droit_image_data
    )
    db.session.add(espece)
    db.session.commit()
    return render_template('charger19.html', filename=filename_data)


@app.route('/display/<filename>')
# affiche l'image depuis le repertoire static
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/modifier/<especeid>')
def espece_modif(especeid):
    #photo = Photo.query.filter(id=photoid)
    espece = Espece.query.get(especeid)
    return render_template('modifier2.html', espece=espece)

@app.route('/regne/<int:id>')
# permet de trier les espèces selon leur règne (animal ou vegetal):
# id=0 renvoie toutes les espèces
# id=1 renvoie les espèces du règne animal
# id=1 renvoie les espèces du règne vegetal

def regne(id):
    especes = []
    if id == 0:
        especes = Espece.query.all()
    elif id == 1:
        especes = Espece.query.filter(Espece.regne.like("animal")).all()
    elif id == 2:
        especes = Espece.query.filter(Espece.regne.like("vegetal")).all()
    else:
        especes = []
    return render_template('regne.html', especes=especes)


@app.route("/connexion")
def connexion():
    data = request.form  # c'est un tableau associatif (clé-valeur) appelé collection en python, ou dictionnaire de données
    email_data = data["email"]
    motDePasse_data = data["mdp"]

    compte = Compte(
        email=email_data,
        mdp=motDePasse_data
    )
    #db.session.add(compte)
    #db.session.commit()
    return render_template('form_connexion.html', email=email_data, mdp=motDePasse_data)


@app.route('/apropos')
def page_apropos():
    return render_template('apropos.html')


if __name__ == "__main__":
    app.run(debug=True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#OBJECTIFS DU 15 MARS 2022:
# - terminer de mettre les champs pour toutes les colonnes de la base dans upload
# - réaranger la redirection après les résultats
# - bien déterminer ce que je veux faire avec mon appli (photo ou pas ?)
